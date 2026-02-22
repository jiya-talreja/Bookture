import pymupdf # pyright: ignore[reportMissingImports]
from typing import List
from collections import Counter
import re
def remove_h_f(page):
    head_ratio=0.12
    foot_ratio=0.12
    page_height=page.rect.height
    re_r_h=page_height*head_ratio
    re_r_f=page_height*(1-foot_ratio)
    blocks=page.get_text("blocks")
    paragraphs=[]
    for block in blocks:
        x0,y0,x1,y1,text,*_=block
        if y1<re_r_h:
            continue
        if y0> re_r_f:
            continue
        cleaned = text.strip()
        # ignore junk blocks
        if len(cleaned.split()) < 8:
            continue
        paragraphs.append(cleaned)
    return paragraphs
def get_text(file_path: str):
    doc = pymupdf.open(file_path)
    chppage = toc_extract(doc)   # chapter start page
    page_count = doc.page_count
    extracted_pages = []
    for i in range(chppage, page_count):
        page = doc.load_page(i)
        paragraphs = remove_h_f(page)
        extracted_pages.append({
            "pageno": i + 1,
            "paragraphs": paragraphs
        })
    return extracted_pages
FRONT_MATTER = {
    "title",
    "copyright",
    "contents",
    "introduction",
    "preface",
    "foreword",
    "acknowledgements",
    "publisher's preface",
    "author's preface"
}
CHAPTER_PATTERNS = [
    r"^1[\.\s]",              # 1. or 1 
    r"^chapter\s+1\b",        # chapter 1
    r"^chapter\s+one\b",      # chapter one
    r"^i[\.\s]",              # i. or i  (roman)
]
def is_probable_chapter_one(level:int,title: str, page: int,level1_count:int) -> bool:
    t = title.lower().strip()
    #Reject front matter
    if t in FRONT_MATTER:
        return False
    #Reject questions
   
    #Reject long titles (likely subsection)
    if len(t) > 60:
        return False
    #Page number sanity check
    if page < 2:   # chapters rarely start at page < 5
        return False
    #Must match strict chapter patterns
    for pattern in CHAPTER_PATTERNS:
        if re.match(pattern, t):
            return True
    if (
        level == 1 and
        level1_count > 1 and      # must be part of a sequence
        page >= 10 and            # avoid preface/introduction
        t not in FRONT_MATTER
    ):
        return True
    return False
def word_count(text:str)->bool:
    return len(text.split())
def toc_extract(doc):
    toc=doc.get_toc()
    f_w=["prepared and published by","translated by"]
    if not toc:
        print("NO TOC")
        for i in range(20):
            page=doc.load_page(i)
            text=page.get_text()
            wc = word_count(text)
            if wc < 60:
                continue
            text = text.lower()
            if any(word in text for word in FRONT_MATTER or f_w):
                continue
            print(f"Content starts at page {i+1}, word count = {wc}")
            return i
        return 0    
    level1_count = sum(
        1 for item in toc
        if isinstance(item, (list, tuple)) and len(item) >= 3 and item[0] == 1
    )
    #to identity is toc a tuple
    for item in toc:#check fro every item
        if not isinstance(item,(list,tuple)) and len(item)<3:#if not a list or tuple or has len less than 3 skip
            print("A")
            continue
        level,title,pageno=item[0],item[1],item[2]
        if not isinstance(title,str) and not isinstance(pageno,int):
            print("3")
            continue
        if is_probable_chapter_one(level,title, pageno,level1_count):
            print("page number : ",pageno-1)
            print("title : ",title)
            return pageno - 1  # zero-based index
    return 0
# for getting text of padf page wise removing noises and starting from first pafe of chp    