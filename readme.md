1. gpdvox.py
# for CLI use. chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first
# voicevox engine is required.

------------------------

2. gpt_flask.py
# simple flask API for chatgpt_wrapper, to be used with voicevox 春日部つむぎ
# chatgpt_wrapper is required and need to authenticate with chatgpt_wrapper first
# should run before client.py
# python gpt_flask.py

3. client.py
# simple chatbot frontend powered by streamlit, only for voicevox 春日部つむぎ chatbot
# voicevox engine and gpt_flask.py are required
# streamlit run client.py