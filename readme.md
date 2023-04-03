# overview

<strong>
이번 업데이트로, OpenAI 유료 API키가 필요해졌습니다.  
유료 API키를 쓰지 않으실 분들은 using-chatgpt-wrapper(legacy) 브랜치의 구버전을 이용해주세요.  
Now you need OpenAI paid API key.  
If you don't want to pay for API, use "using-chatgpt-wrapper(legacy)" branch.  
今回のアップデートで、OpenAIの有料APIキーが必要になりました。  
有料APIキーを使いたくない方は、using-chatgpt-wrapper(legacy)の旧バージョンをお使いください。
</strong>

ChatGPT에 voicevox 여캐들의 설정(혹은 커스텀 설정)을 입력하여 voicevox를 통해 목소리로 읽어주는,  
voicevox 여캐들과 대화를 할 수 있는(것 같은 기분이 드는) 음성 달린 챗봇입니다.  
파이썬은 처음 써보는거라 혼자 쓸 용으로 진짜 개발새발 대충 만들었는데 보관용으로 업로드. 일단 작동은 합니다.  
프롬프트에 개선의 여지 있음. tumugi.db 파일에 sqlite로 기본 프롬프트 저장되어있으니 맘에 안드시면 수정해서 이용하세요.

Input voivevox characters' profile(or own custom profile) to ChatGPT, and talk to her(sort of), with voice via voicevox.  
First attempt using python, and roughly made for my own use, it works anyway.    
default character promps are stored in tumugi.db, you can amend it as you wish.

ChatGPTにvoicevoxキャラのプロフィールを入れ、Voivevoxを通じて彼女たちの声でおしゃべりしてくれます。  
ボイボたちと会話を楽しめる（風の）声付きチャットボットです。今んとこ女子のみです。  
Pythonは初めてで、自分用でかなりいい加減な作りです。一応、動きます。  
プロンプトに改善の余地ありです。デフォルトのキャラプロンプトはsqliteでtumugi.dbに格納されていますが、好きなように修正してお使いください。


# how to use
1. install python
2. (optional) set venv or conda or whatever
3. download and run voicevox engine https://github.com/VOICEVOX/voicevox_engine/releases/latest
4. set your paid OpenAI API Key in get_api.py(openai.api_key = "SET_YOUR_API_KEY_HERE")
5. install streamlit and option menu: pip install streamlit streamlit_option_menu
6. streamlit run client.py  


# screenshots

アップデートで会話履歴、速さ調整、返信再生成、送信取り消しが追加されました。  
<img src=https://user-images.githubusercontent.com/70783505/229495448-ab302f50-d0b6-4b5c-b570-9c1c4a8e04ab.png width="60%" height="60%" />

１．メイン画面  
<img src=https://user-images.githubusercontent.com/70783505/229291536-586afcd1-e3e7-490d-a49c-fc33a97458e6.png width="60%" height="60%" />
  
２．音声選択  
<img src=https://user-images.githubusercontent.com/70783505/229291539-e3f296dd-03b7-4c6f-8119-181aabdb5f23.png width="60%" height="60%" />
  
３．キャラカスタマイズ  
<img src=https://user-images.githubusercontent.com/70783505/229291541-7cfef919-391e-4801-82e5-113b17a875d9.png width="60%" height="60%" />
  
４．会話（音声リプレイ付き）  
<img src=https://user-images.githubusercontent.com/70783505/229291988-36f43073-ca17-4d75-9f24-b17a8064fdbd.png width="60%" height="60%" />
  
------------------------

# 1. gpt_flask.py
simple flask API for chatgpt_wrapper, to be used with voicevox 
chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first  
should run before client.py  
python gpt_flask.py  

# 2. client.py
simple chatbot frontend powered by streamlit, only for voicevox chatbot  
voicevox engine and gpt_flask.py are required  
streamlit run client.py  
