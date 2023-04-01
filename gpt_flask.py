# simple flask API for chatgpt_wrapper, to be used with voicevox
# chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first
# should run before client.py
# python gpt_flask.py

from chatgpt_wrapper import ChatGPT
from chatgpt_wrapper.core.config import Config

from flask import Flask,request

config = Config()
bot = ChatGPT(config)
app = Flask(__name__)

@app.route('/bot-reinit')
def botReinit():
    name = request.args.get('name', '女の子')
    info = request.args.get('info', '')
    bot.new_conversation()
    return initText(name, info)

@app.route('/init-text')
def initText(name, info):
    prompt = f"あなたは、「{name}」という名前の女の子です。以下、キャラクターに関する情報を与えます。{info}以上のことを踏まえて、{name}というキャラクターを最後まで演じ切りなさい。台詞のサンプルがある場合、あくまでも口調の参考程度にお使いください。もし、与えられた名前と台詞のサンプルが食い違っている場合、与えられたキャラクターの名前を優先してください。それでは、まずは自己紹介からお願いします。"
    success, response, message = bot.ask(prompt)
    
    if success:
        return response
    else:
        raise RuntimeError(message)

@app.route('/talk-text', methods=['POST'])
def talkText():  
    json_data = request.json
    text = json_data.get('text', '')
        
    success, response, message = bot.ask(text)
    if success:
        return response
    else:
        raise RuntimeError(message)

if __name__ == '__main__':
    app.run(host='localhost', port=3000, threaded=False)

