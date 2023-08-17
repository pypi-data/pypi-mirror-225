from wombo import Dream

def draw(prompt : str, style : int):
    dream = Dream()
    img = dream.generate(prompt, style)
    return img.photo_url_list[0]