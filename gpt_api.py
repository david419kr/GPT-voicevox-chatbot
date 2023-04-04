import openai
openai.api_key = "SET_YOUR_API_KEY_HERE"

model = "gpt-3.5-turbo"

def initBot(name, info):
    messages = [{
            "role": "system",
            "content": f"あなたは、「{name}」という名前の女の子です。以下、キャラクターに関する情報を与えます。{info}以上のことを踏まえて、{name}というキャラクターを最後まで演じ切りなさい。台詞のサンプルがある場合、あくまでも口調の参考程度にお使いください。もし、与えられた名前と台詞のサンプルが食い違っている場合、与えられたキャラクターの名前を優先してください。"
        },
        {
            "role": "user",
            "content": "まずは、自己紹介からお願いします。"
        }]

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def talkBot(text, messages):
    messages.append({"role": "user", "content": text})

    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
    except:
        messages.pop(1)
        messages.pop(1)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
    if completion.usage.prompt_tokens >= 3600:
        messages.pop(1)  
    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def regenerate(messages):
    messages.pop()
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
    except:
        messages.pop(1)
        messages.pop(1)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
    print(completion.usage.prompt_tokens)
    if completion.usage.prompt_tokens >= 3600:
        messages.pop(1)    
    chat_response = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": chat_response})
    return chat_response, messages

def edit(messages):
    messages.pop()
    messages.pop()
    return messages