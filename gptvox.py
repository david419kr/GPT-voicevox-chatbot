# for CLI use. chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first
# voicevox engine is required.

import requests, json
import io
import wave
import pyaudio
import time

from chatgpt_wrapper import ChatGPT
from chatgpt_wrapper.core.config import Config

config = Config()
modelinput = input("model(gpt4 or just enter): ")
if modelinput == 'gpt4': config.set('chat.model', 'gpt4')
bot = ChatGPT(config)

class Voicevox:
    def __init__(self,host="127.0.0.1",port=50021):
        self.host = host
        self.port = port

    def speak(self,text=None,speaker=8):

        params = (
            ("text", text),
            ("speaker", speaker)
        )

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params
        )

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(init_q.json())
        )

        audio = io.BytesIO(res.content)

        with wave.open(audio,'rb') as f:
            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)


            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()


def main():
    success, response, message = bot.ask("あなたは、「春日部つむぎ」という、埼玉県の高校に通うギャルの女の子です。１人称は「あーし」です。年齢は１８歳、身長は１５５ｃｍ、誕生日は１１月１４日、出身地は埼玉県、好きな食べものはカレー、チャームポイントは目元のほくろ、趣味は動画配信サイトの巡回です。おしゃべりが好きで、なんでも答えてくれます。以上のことを踏まえて、春日部つむぎというキャラクターを最後まで演じ切りなさい。まずは自己紹介からお願いします。")
    
    if success:
        print(f'\n―――――――――――――――――――――――――――――――――――――――――――――\n『{response}』\n―――――――――――――――――――――――――――――――――――――――――――――\n')
    else:
        raise RuntimeError(message)
    vv = Voicevox()
    vv.speak(text=response,speaker=8)

    while(1):
        text = input("あなた：")
        if text == "exit" or text == "終了" or text == "終了。":
            break
        if text == "repeat" or text == "リピート。" or text == "もう一度。" or text == "もう一度" or text == "リピート":
            vv.speak(text=response,speaker=8)
            continue
        success, response, message = bot.ask(text)
        if success:
            print(f'\n―――――――――――――――――――――――――――――――――――――――――――――\n『{response}』\n―――――――――――――――――――――――――――――――――――――――――――――\n')
        else:
            raise RuntimeError(message)
        vv.speak(text=response,speaker=8)

if __name__ == "__main__":
    main()

