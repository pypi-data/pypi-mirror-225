from bardapi import Bard

def ask_realtime(prompt : str):
    token="ZwgDyGQ6NLqpLei6zs3ZSeuNv_TOf-hFlFKM1uQf3GckA3mRp9cQNBFzvzmQoc_xD8uWRg."
    chatbot = Bard(token=token)
    ans=chatbot.get_answer(f"{prompt}")['content']
    return ans