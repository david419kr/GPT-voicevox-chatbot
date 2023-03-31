# simple chatbot frontend powered by streamlit, only for voicevox 春日部つむぎ chatbot
# voicevox engine and gpt_flask.py are required
# streamlit run client.py

import streamlit as st
import requests, json, base64, sqlite3
import streamlit.components.v1 as components

conn = sqlite3.connect('tumugi.db')

c = conn.cursor()
c.execute("SELECT * FROM chats ORDER BY id DESC LIMIT 1")
latest_row = c.fetchone()

if latest_row:
    chat_history = st.session_state.get("chat_history", [])
    chat_history = json.loads(latest_row[1])
    st.session_state.chat_history = chat_history
else:
    chat_history = st.session_state.get("chat_history", [])

BASE_URL = "http://localhost:"
FLASK_PORT = "3000"
VOICEVOX_PORT = "50021"
VOICEVOX_FIRST_ENDPOINT = "/audio_query"
VOICEVOX_SECOND_ENDPOINT = "/synthesis"

st.title("つむぎちゃんとおしゃべり！")

def generate_voice(text):
    params = (
        ("text", text),
        ("speaker", 8)
    )
    pre_voice = requests.post(
        BASE_URL + VOICEVOX_PORT + VOICEVOX_FIRST_ENDPOINT,
        params=params).json()
    voice = requests.post(BASE_URL + VOICEVOX_PORT + VOICEVOX_SECOND_ENDPOINT,
                  headers={"Content-Type": "application/json"},
                  params = params,
                  data=json.dumps(pre_voice))
    b64 = base64.b64encode(voice.content).decode()
    md = f"""
            <audio control autoplay="true">
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            </audio>
            """
    
    components.html(md + "<style>audio{display:none;}</style>", height=0)
    b64 = ''


if st.button("新しい会話を始める"):
    chat_history = []
    with st.spinner("つむぎちゃんが自己紹介するよ..."):
        text = requests.get(BASE_URL + FLASK_PORT + '/bot-reinit').content.decode('utf-8')
        chat_history.append(f'<span style="color:#fff5b1">**つむぎ**</span>： {text}')
        c.execute("UPDATE chats SET chat_history = ? WHERE id = ?", (json.dumps(chat_history), latest_row[0]))
        conn.commit()
        generate_voice(text)
    st.session_state.chat_history = chat_history

with st.form(key="form", clear_on_submit=True):
    if not chat_history:
        user_input = st.text_area("あなた： ", key="disabled", value="", disabled=True)
    else:
        user_input = st.text_area("あなた： ", key="enabled", value=st.session_state.get("user_input", ""))

    def clear_text():
        st.session_state["enabled"] = ""

    def generate_response(user_input):
        response = requests.post(BASE_URL + FLASK_PORT + "/talk-text", json={"text": user_input}).content.decode('utf-8')
        return response

    if st.form_submit_button(label="送信"):
        if user_input:
            chat_history.append(f'<span style="color:skyblue">**あなた**</span>： {user_input}')
            st.session_state.chat_history = chat_history
            
            with st.spinner("つむぎちゃんが考えているよ..."):
                text = generate_response(user_input)
                chat_history.append(f'<span style="color:#fff5b1">**つむぎ**</span>： {text}')
                #play voice
                generate_voice(text)
                c.execute("UPDATE chats SET chat_history = ? WHERE id = ?", (json.dumps(chat_history), latest_row[0]))
                conn.commit()
            st.session_state.chat_history = chat_history
            st.session_state.user_input = ""


if "chat_history" in st.session_state:
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f'{chat}', unsafe_allow_html=True)