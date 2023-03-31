ChatGPT에 카스카베 츠무기의 프로필을 입력한 후, voicevox를 통해 카스카베 츠무기의 목소리로 읽어주는,  
카스카베 츠무기와 대화를 할 수 있는(풍의) 챗봇입니다.  
변수와 기본 프롬프트를 변경하면 voicevox의 다른 캐릭터도 가능합니다.  
혼자 쓸 용으로 대충 만들었는데 보관용으로 업로드. 일단 작동은 합니다.  

Input Kasukabe Tsumugi's profile to ChatGPT, and talk to her(sort of), with voice via voicevox.  
Can use for other voicevox characters, if you change variables and prompt.  
Made for my own use, it works anyway.    

ChatGPTに春日部つむぎのプロフィールを入れ、Voivevoxを通じて彼女の声でおしゃべりしてくれます。  
つむぎちゃんとの会話を楽しめる（風の）チャットボットです。  
変数やプロンプトを弄ると、Voicevoxの他キャラにも使えます。  
自分用でかなりいい加減な作りです。一応、動きます。  

[![동작 영상](https://i9.ytimg.com/vi_webp/QkXCQ3p3yTo/sddefault.webp?v=64267aa0&sqp=COT0maEG&rs=AOn4CLAjUVLXhnd0PjQghTH61oItQ-9YTA)](https://www.youtube.com/watch?v=QkXCQ3p3yTo)

------------------------

# 1. gpdvox.py
for CLI use. chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first  
voicevox engine is required.  

------------------------

# 2. gpt_flask.py
simple flask API for chatgpt_wrapper, to be used with voicevox 春日部つむぎ  
chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first  
should run before client.py  
python gpt_flask.py  

# 3. client.py
simple chatbot frontend powered by streamlit, only for voicevox 春日部つむぎ chatbot  
voicevox engine and gpt_flask.py are required  
streamlit run client.py  
