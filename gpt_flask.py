# simple flask API for chatgpt_wrapper, to be used with voicevox 春日部つむぎ
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
    bot.new_conversation()
    return initText()

@app.route('/init-text')
def initText():
    success, response, message = bot.ask("あなたは、「春日部つむぎ」という、埼玉県の高校に通うギャルの女の子です。１人称は「あーし」です。年齢は１８歳、身長は１５５ｃｍ、誕生日は１１月１４日、出身地は埼玉県、好きな食べものはカレー、チャームポイントは目元のほくろ、趣味は動画配信サイトの巡回です。おしゃべりが好きで、なんでも答えてくれます。以上のことを踏まえて、春日部つむぎというキャラクターを最後まで演じ切りなさい。まずは自己紹介からお願いします。")
    
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

