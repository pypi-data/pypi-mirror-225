from wombo import Dream

def draw(prompt : str, style : int, api_key : str):
    if api_key=="vanshshah1029384756":
        dream = Dream()
        img = dream.generate(prompt, style)
        return img.photo_url_list[0]
    else:
        return "invalid api key you dumbasssss!"