# update 241205

*ChatGPT以外に、Grok APIとOllamaに対応しました。  
*モデルの会話温度を設定できるようになりました。   
*GUI上でAPIキーを設定できるようになりました。   
*環境変数にOPENAI_API_KEYやXAI_API_KEYが設定されていたら、自動で読み込むようになりました。   


# overview

ChatGPTやGrok、Ollamaにvoicevoxキャラのプロフィールを入れ、Voivevoxを通じて彼女たちの声でおしゃべりしてくれます。  
ボイボたちと会話を楽しめる（風の）声付きチャットボットです。今んとこ女子のみです。  
Pythonは初めてで、自分用でかなりいい加減な作りです。一応、動きます。  
プロンプトに改善の余地ありです。デフォルトのキャラプロンプトはsqliteでtumugi.dbに格納されていますが、好きなように修正してお使いください。  
ちなみに、会話履歴やオプションの選択時に、２回クリックしないと反映されたりされなかったりするバグがありますが、解決法が分かりません。


# how to use
1. Pythonをインストールします。（3.10で動作確認しました）
2. このレポジトリーをgit cloneするか、[Download ZIP](https://github.com/david419kr/GPT-voicevox-chatbot/archive/refs/heads/main.zip)します。
3. [Voicevox Engine](https://github.com/VOICEVOX/voicevox_engine/releases/latest)をインストールします。
4. 左上の設定メニューで、APIキーを入れます。Ollamaのみ使う場合はスルーで。
![image](https://github.com/user-attachments/assets/85cea092-1aba-4496-9e53-256121cb1e05)

5. "start.bat"で起動します。初起動の場合、自動でvenvが生成されインストールされます。


# screenshots  

１．メイン画面  
![image](https://github.com/user-attachments/assets/0cf87397-66dc-4abe-8d63-838762d62d9b)

  
２．音声選択  
![image](https://github.com/user-attachments/assets/f2bb5bc5-8a1f-4fd4-b540-381869fa973f)

  
３．キャラカスタマイズ  
![image](https://github.com/user-attachments/assets/45d5b394-576e-456d-bee5-c7a58712b350)

  
４．API、モデル選び  
![image](https://github.com/user-attachments/assets/8c46284c-56c2-4f3b-8e6e-932fda106314)

5. 会話（音声リプレイ付き）  
![image](https://github.com/user-attachments/assets/4a75cfef-7b3f-414e-8086-afe1b2e92fc6)


