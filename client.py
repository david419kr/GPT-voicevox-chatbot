# simple chatbot frontend powered by streamlit, for voicevox chatbot
# voicevox engine and gpt_flask.py are required
# streamlit run client.py

import streamlit as st
import requests, json, base64, sqlite3
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

import gpt_api

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

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

c.execute("SELECT * FROM chats WHERE is_current_chat = 1")
current_chat = c.fetchone()

c.execute("SELECT * FROM girl_settings")
girl_settings = c.fetchone()
current_speaker = girl_settings[1]
current_custom_name = girl_settings[2]
is_custom_name = girl_settings[3]
current_speed = girl_settings[4]

speaker_index = speaker_list.index(current_speaker)

with st.sidebar:
    st.markdown("""リストをダブルクリックしてね。  
    新しい会話はリロードで反映されるよ。""")
    if st.button("↻ リロード"):
        st.experimental_rerun()
    c.execute("SELECT * FROM chats WHERE id != 1")
    all_chat = c.fetchall()
    
    if len(all_chat) != 0:
        current_chat_index = next(i for i, el in enumerate(all_chat) if el[6] == 1)

        selected = option_menu(
            menu_title="会話履歴",
            options=[(f"{chat[0]-1}. {chat[4]}") for chat in all_chat],
            default_index=current_chat_index,
        )
        
        selected_id = int(selected.split(".")[0]) + 1

        c.execute("UPDATE chats SET is_current_chat = 0 WHERE id = ?", (all_chat[current_chat_index][0],))
        conn.commit()
        c.execute("UPDATE chats SET is_current_chat = 1 WHERE id = ?", (selected_id,))
        conn.commit()
        speaker_index = speaker_list.index(all_chat[selected_id-2][2])
    else:
        st.markdown("まだ会話履歴がありません。")

if current_chat:
    chat_history = st.session_state.get("chat_history", [])
    chat_history = json.loads(current_chat[1])
    st.session_state.chat_history = chat_history
    api_messages = json.loads(current_chat[5])
    speaker_index = speaker_list.index(current_chat[2])
else:
    chat_history = st.session_state.get("chat_history", [])
    api_messages = []
    is_custom_name = 0

BASE_URL = "http://localhost:"
VOICEVOX_PORT = "50021"
VOICEVOX_FIRST_ENDPOINT = "/audio_query"
VOICEVOX_SECOND_ENDPOINT = "/synthesis"

st.title(f"VOICEVOX女子とおしゃべり！")

def generate_voice(text, speed):
    params = (
        ("text", text),
        ("speaker", speaker)
    )
    pre_voice = requests.post(
        BASE_URL + VOICEVOX_PORT + VOICEVOX_FIRST_ENDPOINT,
        params=params).json()
    pre_voice['speedScale'] = speed
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

col8, col9 = st.columns([0.7,0.3])
speaker_name = col8.selectbox(
    "女の子を選んでね",
    speaker_nametag,
    index=speaker_index
)
speaker_index = speaker_nametag.index(speaker_name)
speaker = speaker_list[speaker_index]

voice_speed = col9.slider("話す速さを調整してね", min_value=0.5, max_value=2.0, value=current_speed, step=0.1)
c.execute("UPDATE girl_settings SET speed = ? where id = ?", (voice_speed, girl_settings[0]))

if st.checkbox("好きな名前をつける", value=is_custom_name):
    st.markdown(""":orange[新しい会話を始めると反映されます。チェックを外すと元の名前に戻ります。  
    キャラの基本設定と衝突する場合、カスタムキャラ設定の完全上書き推奨。]""")
    name = st.text_input("名前を入力してね", value=current_custom_name)
    c.execute("UPDATE girl_settings SET is_custom_name = ? where id = ?", (1, girl_settings[0]))
    c.execute("UPDATE girl_settings SET custom_name = ? where id = ?", (name, girl_settings[0]))
    conn.commit()
else:
    name = speaker_name.split()[0]
    c.execute("UPDATE girl_settings SET is_custom_name = ? where id = ?", (0, girl_settings[0]))
    conn.commit()
c.execute("UPDATE girl_settings SET speaker = ? where id = ?", (speaker, girl_settings[0]))
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
        text, api_messages = gpt_api.initBot(name, info)
        chat_history.append(f'<span style="color:#fff5b1"><strong>{name}</strong></span>： {text}')
        c.execute("UPDATE chats SET is_current_chat = ? WHERE id = ?", (0, current_chat[0]))
        conn.commit()
        c.execute("INSERT INTO chats (is_current_chat, speaker, is_custom_name, custom_name, chat_history, api_messages) VALUES (?, ?, ?, ?, ?, ?)", (1, speaker, is_custom_name, name, json.dumps(chat_history), json.dumps(api_messages)))
        conn.commit()
        current_chat = c.execute("SELECT * FROM chats WHERE is_current_chat = 1").fetchone()
        conn.commit()
        generate_voice(text, voice_speed)
    st.session_state.chat_history = chat_history

with st.form(key="form", clear_on_submit=True):
    if not chat_history:
        user_input = st.text_area("あなた： ", key="disabled", value="", disabled=True)
    else:
        user_input = st.text_area("あなた： ", key="enabled", value=st.session_state.get("user_input", ""))

    def clear_text():
        st.session_state["enabled"] = ""

    def generate_response(user_input, api_messages):
        response, api_messages = gpt_api.talkBot(user_input, api_messages)
        return response, api_messages
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 0.6, 1, 0.5, 0.5, 0.5, 0.5])

    if col1.form_submit_button(label="送信"):
        if user_input:
            chat_history.append(f'<span style="color:skyblue"><strong>あなた</strong></span>： {user_input}')
            st.session_state.chat_history = chat_history
            
            with st.spinner(f"{current_chat[4]}が考えているよ..."):
                text, api_messages = generate_response(user_input, api_messages)
                chat_history.append(f'<span style="color:#fff5b1"><strong>{current_chat[4]}</strong></span>： {text}')
                #play voice
                generate_voice(text, voice_speed)
                c.execute("UPDATE chats SET chat_history = ? WHERE id = ?", (json.dumps(chat_history), current_chat[0]))
                c.execute("UPDATE chats SET api_messages = ? WHERE id = ?", (json.dumps(api_messages), current_chat[0]))
                conn.commit()
            st.session_state.chat_history = chat_history
            st.session_state.user_input = ""

    if col2.form_submit_button("再生成"):
        with st.spinner(f"{current_chat[4]}が考えているよ..."):
            response, api_messages = gpt_api.regenerate(api_messages)
            chat_history.pop()
            chat_history.append(f'<span style="color:#fff5b1"><strong>{current_chat[4]}</strong></span>： {response}')
            #play voice
            generate_voice(response, voice_speed)
            c.execute("UPDATE chats SET chat_history = ? WHERE id = ?", (json.dumps(chat_history), current_chat[0]))
            c.execute("UPDATE chats SET api_messages = ? WHERE id = ?", (json.dumps(api_messages), current_chat[0]))
            conn.commit()
        st.session_state.chat_history = chat_history
    
    if col3.form_submit_button("送信取り消し"):
        if len(chat_history) > 1:
            api_messages = gpt_api.edit(api_messages)
            chat_history.pop()
            chat_history.pop()
            st.session_state.chat_history = chat_history
            c.execute("UPDATE chats SET chat_history = ? WHERE id = ?", (json.dumps(chat_history), current_chat[0]))
            c.execute("UPDATE chats SET api_messages = ? WHERE id = ?", (json.dumps(api_messages), current_chat[0]))
            conn.commit()
        else:
            st.warning("直近の送信がありません")


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
                with st.spinner(f"{current_chat[4]}が読み上げているよ..."):
                    pre_voice = requests.post(
                        BASE_URL + VOICEVOX_PORT + VOICEVOX_FIRST_ENDPOINT,
                        params=params).json()
                    pre_voice['speedScale'] = voice_speed
                    voice = requests.post(BASE_URL + VOICEVOX_PORT + VOICEVOX_SECOND_ENDPOINT,
                                headers={"Content-Type": "application/json"},
                                params = params,
                                data=json.dumps(pre_voice))
                    st.audio(voice.content, format='audio/wav', start_time=0)
        i+=1

