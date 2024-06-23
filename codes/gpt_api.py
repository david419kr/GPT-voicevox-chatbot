import openai
import requests

with open("SET_YOUR_API_KEY_HERE.txt", 'r', encoding='utf-8') as file:
    api_key = file.readline().strip()

openai.api_key = api_key

url = "https://api.openai.com/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}"
}
response = requests.get(url, headers=headers)
models = []
if response.status_code == 200:
    get_models = response.json()["data"]
    for model in get_models:
        if model['id'][:3] == "gpt":
            models.append(model['id'])
else:
    print("Failed to fetch models:", response.status_code, response.text)
    models = ["gpt-4o", "gpt-3.5-turbo-16k"]

# print(models)

temperature = 1.0

def initBot(name, info, model):
    currentModel = model
    messages = [{
            "role": "system",
            "content": f"あなたは、「{name}」という名前の女の子です。以下、キャラクターに関する情報を与えます。{info}以上のことを踏まえて、{name}というキャラクターを最後まで演じ切りなさい。"
        },
        {
            "role": "user",
            "content": "まずは、自己紹介からお願いします。"
        }]

    completion = openai.ChatCompletion.create(
        model=currentModel,
        messages=messages,
        temperature=temperature,
    )

    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def talkBot(text, messages, model):
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

def regenerate(messages, model):
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


