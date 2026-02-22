import requests
def image_gen(prompt : str):
    url = "https://gateway.pixazo.ai/flux-2-klein-4b/v1/generateImage"
    key="ur_api_key"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": key
    }
    data = {
        "prompt" : prompt,
        "steps": 25,
        "width": 1024,
        "height": 1024
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    print(response.text)
    print(response.status_code)
    text=response.json()
    url=text["output"]
    print(url)
    return url
