from bardapi import Bard
def ask_image(image : str, prompt : str,  api_key : str):
    if api_key=="vanshshah1029384756":
        token="ZwgDyGQ6NLqpLei6zs3ZSeuNv_TOf-hFlFKM1uQf3GckA3mRp9cQNBFzvzmQoc_xD8uWRg."
        chatbot = Bard(token=token)
        img = open(image, 'rb').read()
        ans = chatbot.ask_about_image(prompt, img)
        return ans
    else:
        return "invalid api key you dumbasssss!"