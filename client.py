# simple chatbot frontend powered by streamlit, for voicevox chatbot
# voicevox engine and gpt_flask.py are required
# streamlit run client.py

import streamlit as st
import requests, json, base64, sqlite3
import streamlit.components.v1 as components

girls = {
    "四国めたん": {
        "ノーマル": 2,
        "あまあま": 0,
        "ツンツン": 6,
        "セクシー": 4,
        "ささやき": 36,
        "ヒソヒソ": 37,
    },
    "ずんだもん": {
        "ノーマル": 3,
        "あまあま": 1,
        "ツンツン": 7,
        "セクシー": 5,
        "ささやき": 22,
        "ヒソヒソ": 38,
    },
    "春日部つむぎ": {
        "ノーマル": 8,
    },
    "雨晴はう": {
        "ノーマル": 10,
    },
    "波音リツ": {
        "ノーマル": 9,
    },
    "冥鳴ひまり": {
        "ノーマル": 14,
    },
    "九州そら": {
        "ノーマル": 16,
        "あまあま": 15,
        "ツンツン": 18,
        "セクシー": 17,
        "ささやき": 19,
    },
    "もち子さん": {
        "ノーマル": 20,
    },
    "WhiteCUL": {
        "ノーマル": 23,
        "たのしい": 24,
        "かなしい": 25,
        "びえーん": 26,
    },
    "後鬼": {
        "人間ver.": 27,
        "ぬいぐるみver.": 28,
    },
    "No.7": {
        "ノーマル": 29,
        "アナウンス": 30,
        "読み聞かせ": 31,
    },
    "櫻歌ミコ": {
        "ノーマル": 43,
        "第二形態": 44,
        "ロリ": 45,
    },
    "小夜": {
        "ノーマル": 46,
    },
    "ナースロボ＿タイプＴ": {
        "ノーマル": 47,
        "楽々": 48,
        "恐怖": 49,
        "内緒話": 50,
    },
    "春歌ナナ": {
        "ノーマル": 54,
    },
    "猫使ビィ": {
        "ノーマル": 58,
        "おちつき": 59,
        "人見知り": 60,
    },
}

speaker_list = []
speaker_nametag = []
for girl in girls:
    for style in girls[girl]:
        speaker_list.append(girls[girl][style])
        speaker_nametag.append(girl + " " + style)

conn = sqlite3.connect('tumugi.db')

c = conn.cursor()
c.execute("SELECT * FROM chats ORDER BY id DESC LIMIT 1")
latest_row = c.fetchone()

if latest_row:
    chat_history = st.session_state.get("chat_history", [])
    chat_history = json.loads(latest_row[1])
    st.session_state.chat_history = chat_history
    index = speaker_list.index(latest_row[2])
    is_custom_name = latest_row[3]
else:
    chat_history = st.session_state.get("chat_history", [])
    is_custom_name = 0

BASE_URL = "http://localhost:"
FLASK_PORT = "3000"
VOICEVOX_PORT = "50021"
VOICEVOX_FIRST_ENDPOINT = "/audio_query"
VOICEVOX_SECOND_ENDPOINT = "/synthesis"

st.title(f"VOICEVOX女子とおしゃべり！")

def generate_voice(text):
    params = (
        ("text", text),
        ("speaker", speaker)
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

speaker_name = st.selectbox(
    "女の子を選んでね",
    speaker_nametag,
    index=index
)
speaker_index = speaker_nametag.index(speaker_name)
speaker = speaker_list[speaker_index]
if st.checkbox("好きな名前をつける", value=is_custom_name):
    st.markdown(""":orange[新しい会話を始めると反映されます。チェックを外すと元の名前に戻ります。  
    キャラの基本設定と衝突する場合、カスタムキャラ設定の完全上書き推奨。]""")
    name = st.text_input("名前を入力してね", value=latest_row[4])
    c.execute("UPDATE chats SET is_custom_name = ? where id = ?", (1, latest_row[0]))
    c.execute("UPDATE chats SET custom_name = ? where id = ?", (name, latest_row[0]))
    conn.commit()
else:
    name = speaker_name.split()[0]
    c.execute("UPDATE chats SET is_custom_name = ? where id = ?", (0, latest_row[0]))
    conn.commit()
c.execute("UPDATE chats SET speaker = ? where id = ?", (speaker, latest_row[0]))
conn.commit()

c.execute("SELECT * FROM girls_info WHERE name = ?", (speaker_name.split()[0],))
default_info = c.fetchone()[1]
c.execute("SELECT * FROM girls_info WHERE name = ?", ("custom",))
custom_info = c.fetchone()[1]

info = ''

if st.checkbox(f"カスタムキャラ設定を入力する{custom_info and '　※現在、カスタムキャラ設定が入力されています。'}"):
    st.markdown(""":orange[新しい会話を始めると反映されます。]:red[**チェックを外しても保存されたままなので、**]  
    :orange[基本のキャラ設定に戻したい場合は、テキスト欄を空欄にしてから新しい会話を始めてください。  
    基本のキャラ設定を維持したまま、カスタムのキャラ設定を追加することもできますし、  
    基本のキャラ設定を完全に上書きし、声はそのままで好きなキャラに変身させることもできます。  
    上書きをする場合、下のチェックボックスをチェックしてください。]""")
    custom_info = st.text_area("カスタムキャラ設定を入力してね", value=custom_info)
    c.execute("UPDATE girls_info SET info = ? WHERE name = ?", (custom_info, "custom"))
    conn.commit()
    if st.checkbox("デフォルトのキャラ設定は使わず、完全に上書きする") and custom_info:
        info = custom_info
    else:
        info = default_info + custom_info
if not info:
    info = default_info

if st.button("新しい会話を始める"):
    chat_history = []
    with st.spinner(f"{name}が自己紹介するよ..."):
        text = requests.get(BASE_URL + FLASK_PORT + f'/bot-reinit?name={name}&info=%0D%0A{info}').content.decode('utf-8')
        chat_history.append(f'<span style="color:#fff5b1"><strong>{name}</strong></span>： {text}')
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
            chat_history.append(f'<span style="color:skyblue"><strong>あなた</strong></span>： {user_input}')
            st.session_state.chat_history = chat_history
            
            with st.spinner(f"{name}が考えているよ..."):
                text = generate_response(user_input)
                chat_history.append(f'<span style="color:#fff5b1"><strong>{name}</strong></span>： {text}')
                #play voice
                generate_voice(text)
                c.execute("UPDATE chats SET chat_history = ? WHERE id = ?", (json.dumps(chat_history), latest_row[0]))
                conn.commit()
            st.session_state.chat_history = chat_history
            st.session_state.user_input = ""


if "chat_history" in st.session_state:
    i=0
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f'<div id=chat{i}>{chat}</div>', unsafe_allow_html=True)
        params = (
        ("text", chat.split('： ')[1]),
        ("speaker", speaker)
        )
        if chat.split('： ')[0] != f'<span style="color:skyblue"><strong>あなた</strong></span>':
            tmp = st.empty()
            if tmp.button(f"▶️ リプレイ", str(i)):
                tmp.empty()
                with st.spinner(f"{name}が読み上げているよ..."):
                    pre_voice = requests.post(
                        BASE_URL + VOICEVOX_PORT + VOICEVOX_FIRST_ENDPOINT,
                        params=params).json()
                    voice = requests.post(BASE_URL + VOICEVOX_PORT + VOICEVOX_SECOND_ENDPOINT,
                                headers={"Content-Type": "application/json"},
                                params = params,
                                data=json.dumps(pre_voice))
                    # b64 = base64.b64encode(voice.content).decode()
                    # md = f"""
                    #         <audio control autoplay="true">
                    #         <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                    #         </audio>
                    #         """
                    # st.markdown(md, unsafe_allow_html=True)
                    st.audio(voice.content, format='audio/wav', start_time=0)
        i+=1

