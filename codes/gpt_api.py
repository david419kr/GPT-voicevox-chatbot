import openai
from typing import List
import requests

with open("SET_YOUR_API_KEY_HERE.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    api_key_openai = lines[0].strip() if len(lines) > 0 else None
    api_key_grok = lines[1].strip() if len(lines) > 1 else None

def check_ollama_server() -> bool:
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

class GPTAPIManager:
    API_CONFIGS = {
        "OpenAI": {
            "base_url": "https://api.openai.com/v1"
        },
        "Grok": {
            "base_url": "https://api.x.ai/v1"
        },
        "Ollama": {
            "base_url": "http://localhost:11434/v1"
        }
    }

    def __init__(self, api_type: str):
        self.api_type = api_type
        self.client = self._initialize_client()
        self.available_models = self._get_available_models()

    def _initialize_client(self):
        if self.api_type == "OpenAI":
            openai.api_base = self.API_CONFIGS["OpenAI"]["base_url"]
            openai.api_key = api_key_openai
        elif self.api_type == "Grok":
            openai.api_base = self.API_CONFIGS["Grok"]["base_url"]
            openai.api_key = api_key_grok
        elif self.api_type == "Ollama":
            openai.api_base = self.API_CONFIGS["Ollama"]["base_url"]
            openai.api_key = "ollama"
        return None

    def _get_available_models(self) -> List[str]:
        try:
            models = []
            for model in openai.Model.list()["data"]:
                if self.api_type == "OpenAI":
                    if model['id'][:3] == "gpt":
                        models.append(model['id'])
                else:
                    models.append(model["id"])
                if len(models) == 0:
                    raise Exception(f"有効なモデルが見つかりませんでした。")
            return models
        except Exception as e:
            if self.api_type == "OpenAI":
                return ["gpt-4o-mini", "gpt-4o"]
            elif self.api_type == "Grok":
                return ["grok-beta"]
            elif self.api_type == "Ollama":
                raise Exception(f"有効なモデルが見つかりませんでした。")
            # raise Exception(f"有効なAPIキーが設定されていないか、APIに接続できませんでした。")

    def change_api(self, new_api_type: str):
        if new_api_type == "Ollama" and not check_ollama_server():
            raise Exception("localhost:11434でOllamaが起動していません。")

        self.api_type = new_api_type
        self.client = self._initialize_client()
        self.available_models = self._get_available_models()

    def get_available_models(self) -> List[str]:
        return self.available_models


def initBot(name, info, model, temperature):
    currentModel = model
    messages = [{
            "role": "system",
            "content": f"あなたは、「{name}」という名前の女の子です。以下、キャラクターに関する情報を与えます。{info}以上のことを踏まえて、{name}というキャラクターを最後まで演じ切りなさい。"
        },
        {
            "role": "user",
            "content": "まずは、挨拶からお願いします。"
        }]

    completion = openai.ChatCompletion.create(
        model=currentModel,
        messages=messages,
        temperature=temperature,
    )

    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def talkBot(text, messages, model, temperature):
    messages.append({"role": "user", "content": text})
    currentModel = model
    completion = openai.ChatCompletion.create(
        model=currentModel,
        messages=messages,
        temperature=temperature,
    )
    print(completion.usage.prompt_tokens)
    print(completion.model)

    if completion.usage.prompt_tokens >= 10000:
        messages.pop(1)  
        messages.pop(1)  

    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def regenerate(messages, model, temperature):
    messages.pop()
    currentModel = model
    completion = openai.ChatCompletion.create(
        model=currentModel,
        messages=messages,
        temperature=temperature,
    )
    print(completion.usage.prompt_tokens)
    print(completion.model)

    if completion.usage.prompt_tokens >= 10000:
        messages.pop(1)    
        messages.pop(1)  
    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def edit(messages):
    messages.pop()
    messages.pop()
    return messages


