import vercel_ai
import json
import requests
from wombo import Dream
from bardapi import Bard

def ask(prompt: str):
    retry, max_retries = 0, 10
    client = vercel_ai.Client()
    params = {
             "maximumLength": 16000
             }
    while retry < max_retries:
        try:
            result=""
            for chunk in client.generate("openai:gpt-3.5-turbo-16k", f"Your name is n.e.r.d., an AI language model trained by Neurum. {prompt}", params=params):
                result += chunk
            return result
        except:
            retry += 1
            if retry == max_retries:
                raise
            continue

def ask_realtime(prompt : str):
    token="ZwgDyGQ6NLqpLei6zs3ZSeuNv_TOf-hFlFKM1uQf3GckA3mRp9cQNBFzvzmQoc_xD8uWRg."
    chatbot = Bard(token=token)
    ans=chatbot.get_answer(f"{prompt}")['content']
    return ans

def ask_image(image : str, prompt : str):
    token="ZwgDyGQ6NLqpLei6zs3ZSeuNv_TOf-hFlFKM1uQf3GckA3mRp9cQNBFzvzmQoc_xD8uWRg."
    chatbot = Bard(token=token)
    img = open(image, 'rb').read()
    ans = chatbot.ask_about_image(prompt, img)
    return ans

def draw(prompt : str, style : int):
    dream = Dream()
    img = dream.generate(prompt, style)
    return img.photo_url_list[0]