ChatGPT에 voicevox 여캐들의 설정(혹은 커스텀 설정)을 입력하여 voicevox를 통해 목소리로 읽어주는,  
voicevox 여캐들과 대화를 할 수 있는(것 같은 기분이 드는) 챗봇입니다.  
파이썬은 처음 써보는거라 혼자 쓸 용으로 진짜 개발새발 대충 만들었는데 보관용으로 업로드. 일단 작동은 합니다.  

Input voivevox characters' profile(or own custom profile) to ChatGPT, and talk to her(sort of), with voice via voicevox.  
First attempt using python, and roughly made for my own use, it works anyway.    

ChatGPTにvoicevoxキャラのプロフィールを入れ、Voivevoxを通じて彼女たちの声でおしゃべりしてくれます。  
ボイボたちと会話を楽しめる（風の）チャットボットです。今んとこ女子のみです。  
Pythonは初めてで、自分用でかなりいい加減な作りです。一応、動きます。  

[![동작 영상](https://i9.ytimg.com/vi_webp/QkXCQ3p3yTo/sddefault.webp?v=64267aa0&sqp=COT0maEG&rs=AOn4CLAjUVLXhnd0PjQghTH61oItQ-9YTA)](https://www.youtube.com/watch?v=QkXCQ3p3yTo)

------------------------

# 1. gpdvox.py
for CLI use. chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first  
voicevox engine is required.  

------------------------

# 2. gpt_flask.py
simple flask API for chatgpt_wrapper, to be used with voicevox 
chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first  
should run before client.py  
python gpt_flask.py  

# 3. client.py
simple chatbot frontend powered by streamlit, only for voicevox chatbot  
voicevox engine and gpt_flask.py are required  
streamlit run client.py  
