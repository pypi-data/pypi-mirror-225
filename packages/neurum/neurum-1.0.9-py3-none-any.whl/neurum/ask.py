import vercel_ai
import json
import requests

def ask(prompt: str, api_key : str):
    if api_key=="vanshshah1029384756":
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
    else:
        return "invalid api key you dumbasssss!"