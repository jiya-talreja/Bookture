import spacy # pyright: ignore[reportMissingImports]
nlp = spacy.load("en_core_web_sm")
from image_generation import image_gen
paras=[]
def paras_use(output):
    print(output)
    paras=output.paragraphs
    page_text=",".join(paras)
    doc=nlp(page_text)
    if not paras:
        print("NO paras")
# containers
    characters = set()
    locations = set()
    durations = set()
    seasons = set()#to avoid repeatition
    noun=[]
    verb=[]
    pron=[]
# keyword lists
    duration_words = {"day", "night", "afternoon", "midday", "midnight", "morning", "evening"}
    time={"hour","minute","day"}
    season_words = {"winter", "summer", "rain", "rainy", "mist", "autumn", "snow", "spring"}
    non_verbs = {
    "have","had","is","was","were","do","did","get",
    "say","said","tell","told","think","know","want"
    }
    non_nouns={"girl","girls","boy","boys","eyes","eye","arm","arms"}
# entity extraction
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            characters.add(ent.text)
        elif ent.label_ == "GPE":
            locations.add(ent.text)
    my_set = {"apple", 'ban"ana', "cherry", '"dates"'}

# New set without elements containing "
    characters = {item for item in characters if '"' not in item}        
# keyword-based extraction
    for token in doc:
        word = token.text.lower()
        if token in characters and token.is_alpha == False:
            characters.discard(token)
        if word in duration_words:
            durations.add(word)
        if word in season_words:
            seasons.add(word)
        if token.pos_=="NOUN":
            noun.append(token.text)
        if token.pos_=="PRON":
            pron.append(token.text)
        if token.pos_=="VERB":     
            verb.append(token.text)              
# final structured output
    print("char : ",characters)
    print("location : ",locations)
    print("time : ",duration_words)
    print("sea : ",seasons)
    n_freq={}
    for n in noun:
        n=n.lower()
        if n in n_freq and n not in time | duration_words | characters | non_nouns:
            n_freq[n]+=1
        else:
            n_freq[n]=1
    #phase 1: frequency
    for n in n_freq.copy():
        if n_freq[n]==1:
            del n_freq[n]
    print("frequncy : ",n_freq)   
    noun_info = {}
    for n in n_freq:
        noun_info[n] = {
            "verbs": set(),
            "adjectives": set(),
            "prepositions": set()
        }
    character_info = extract_character_info(doc, characters)
    print("Char info",character_info)    
    #phase 2: imp nouns by dep
    for token in doc:
        word = token.text.lower()
        if word not in noun_info:
            continue
        if token.dep_ in {"nsubj","dobj"} and token.head.pos_ in {"VERB", "ADJ"} and token.text.lower() in n_freq:
            if token.head.pos_ in {"VERB"} and token.head.pos_ not in non_verbs:
                noun_info[word]["verbs"].add(token.head.text)
            else :
                noun_info[word]["adjectives"].add(token.head.text)
        if token.dep_ in {"pobj"} and token.head.pos_ in {"ADP"} and token.text.lower() in n_freq:
            noun_info[word]["prepositions"].add(token.head.text)
        if token.text.lower() in n_freq and token.pos_ == "NOUN":
            for child in token.children:
                if child.dep_ == "amod":
                   noun_info[word]["adjectives"].add(child.text.lower())
    print("NOun info: ",noun_info)   
    print("-------------------------------------------")
    promptt=prompt_try(character_info,characters,locations,seasons,durations,n_freq,doc,noun_info)
    print(promptt)
    url=image_gen(promptt)
    return url
def extract_character_info(doc, character_names):
    character_info = {}
    for char in character_names:
        character_info[char] = {
            "adjectives": set(),
            "verbs": set()
        }
    nv_verbs = {
    "say", "tell", "ask", "know", "think", "feel",
    "fear", "reply", "answer", "explain", "remark","said","told"
    }
    for sent in doc.sents:
        for token in sent:
            # --- CHARACTER NOUN ---
            if token.text in character_names and token.pos_ in {"PROPN", "NOUN"}:
                char = token.text

                # 1) ADJECTIVES: child of character noun
                for child in token.children:
                    if child.dep_ == "amod":
                        if len(character_info[char]["adjectives"]) < 5:
                            character_info[char]["adjectives"].add(child.lemma_.lower())
                head=token.head
                if head.pos_=="ADJ":
                    if len(character_info[char]["adjectives"]) < 3:
                        character_info[char]["adjectives"].add(head.lemma_.lower())
                # 2) VERBS: head of character noun
                head = token.head
                if head.pos_ == "VERB" and head.lemma_.lower() not in nv_verbs:
                    if len(character_info[char]["verbs"]) < 3:
                        character_info[char]["verbs"].add(head.lemma_.lower())
    return character_info
def prompt_try(character_info,characters,locations,seasons,times,n_freq,doc,noun_info):
    selected = []
    for char in characters:
        if character_info[char]["verbs"]:
            selected.append(char)
    prompt= " and ".join(selected)
    #locations :
    if locations:
        loc = next(iter(locations))
        prompt+=" at "+loc    
    else:
        loc = None
    #seasons
    if seasons:
        sea = next(iter(seasons))
        prompt+=" in "+sea
        prompt+=" season "
    else:
        sea = None
    #times
    if times:
        tea = next(iter(times))
        prompt+=" in "+tea
        prompt+=" time "
    else:
        tea = None 
    #location related    
    ll=[]
    non_nouns={"girl","girls","boy","boys","eyes","eye","arm","arms","brains","brain"}
    for n in doc: 
        for keys in n_freq:
            if n.text == keys and n.tag_=="NN" or n.tag_=="NNS" and n.text not in non_nouns:
                ll.append(n.text) 
    ll=set(ll)            
    filtered_ll = {}
    filtered_add={}
    filtered_p={}
    for noun in ll:
        if noun in noun_info:
            if noun_info[noun]["prepositions"]:
                if noun_info[noun]["verbs"]:
                    sets=next(iter(noun_info[noun]["verbs"]))
                    filtered_ll[noun]=sets 
                if noun_info[noun]["adjectives"]:
                    seta=next(iter(noun_info[noun]["adjectives"]))
                    filtered_add[noun]=seta
                setp= next(iter(noun_info[noun]["prepositions"]))
                filtered_p[noun]=setp                
    print("LL : ",ll)
    print("FIltered : ",filtered_ll) 
    print("FIltered : ",filtered_add)
    print("FIltered : ",filtered_p)
    prompt += " with "
    for noun in ll:
        prep = filtered_p.get(noun)
        adj  = filtered_add.get(noun)
        verb = filtered_ll.get(noun)
    # Case 1: all 3
        if adj and verb:
            prompt += f" {adj} {verb} {noun} "
    # Case 2: prep + adj
        elif adj:
            prompt += f" {adj} {noun} "
    # Case 2: prep + verb
        elif  verb:
            prompt += f"{verb} {noun} "
    # Case 2: adj + verb
        elif adj and verb:
            prompt += f"{adj} {verb} {noun} "
    # Case 3: only prep
    # Case 3: only adj
        elif adj:
            prompt += f"{adj} {noun} "
    # Case 3: only verb
        elif verb:
            prompt += f"{verb} {noun} "
    # Case 4: nothing
        else:
            prompt += f"{noun} "
    return prompt
