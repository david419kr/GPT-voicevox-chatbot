# simple chatbot frontend powered by streamlit, for voicevox chatbot
# voicevox engine required
# streamlit run client.py

import streamlit as st
import requests, json, base64, sqlite3
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from streamlit_local_storage import LocalStorage
import json, os
import gpt_api
from gpt_api import GPTAPIManager

localStorage = LocalStorage()

def create_settings_modal():
    with st.sidebar:
        with st.expander("⚙️ APIキー設定", expanded=False):
            OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
            if OPENAI_API_KEY:
                saved_openai_key = OPENAI_API_KEY
                if not localStorage.getItem("openai_api_key"):
                    localStorage.setItem("openai_api_key", saved_openai_key, key="openai_api_key1")
            else:
                saved_openai_key = localStorage.getItem("openai_api_key")
            XAI_API_KEY = os.environ.get("XAI_API_KEY")
            if XAI_API_KEY:
                saved_grok_key = XAI_API_KEY
                if not localStorage.getItem("grok_api_key"):
                    localStorage.setItem("grok_api_key", saved_grok_key, key="grok_api_key1")
            else:
                saved_grok_key = localStorage.getItem("grok_api_key")
            
            openai_key = st.text_input(
                "OpenAI APIキー",
                type="password",
                value=saved_openai_key if saved_openai_key else "",
                key="openai_key_input"
            )
            
            grok_key = st.text_input(
                "Grok APIキー",
                type="password",
                value=saved_grok_key if saved_grok_key else "",
                key="grok_key_input"
            )
            
            if st.button("APIキーを保存する"):
                if openai_key:
                    localStorage.setItem("openai_api_key", openai_key, key="openai_api_key2")
                if grok_key:
                    localStorage.setItem("grok_api_key", grok_key, key="grok_api_key2")
                st.success("APIキーが保存されました。")
                st.rerun()

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

with open('./codes/girls.json', 'r', encoding='utf-8') as file:
    girls = json.load(file)
 
speaker_list = []
speaker_nametag = []
for girl in girls:
    for style in girls[girl]:
        speaker_list.append(girls[girl][style])
        speaker_nametag.append(girl + " " + style)

conn = sqlite3.connect('./codes/tumugi.db')

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
    create_settings_modal()

with st.sidebar:
    if st.button("↻ リロード"):
        st.rerun()
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

def check_voicevox_server() -> bool:
    try:
        response = requests.get(BASE_URL + VOICEVOX_PORT + "/version")
        return response.status_code == 200
    except:
        return False
    
def check_ollama_server() -> bool:
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

st.title(f"VOICEVOX女子とおしゃべり！")

saved_api = localStorage.getItem("selected_api")
saved_model = localStorage.getItem("selected_model")


if 'selected_api' not in st.session_state:
    st.session_state.selected_api = saved_api if saved_api else "OpenAI"

if 'selected_model' not in st.session_state:
    st.session_state.selected_model = saved_model if saved_model else None


col12, col10, col11 = st.columns([0.25, 0.45, 0.3])
api = col12.selectbox(
    "APIを選んでね",
    ["OpenAI", "Grok", "Ollama"],
    index=["OpenAI", "Grok", "Ollama"].index(st.session_state.selected_api),
    key="api_selection"
)

if 'gpt_manager' not in st.session_state:
    st.session_state.gpt_manager = GPTAPIManager(
        api_type=api,
        api_key_openai=localStorage.getItem("openai_api_key"),
        api_key_grok=localStorage.getItem("grok_api_key")
    )

# API変更感知処理
if st.session_state.selected_api != api:
    st.session_state.selected_api = api
    localStorage.setItem("selected_api", api)
    st.session_state.gpt_manager.change_api(api)
    st.session_state.selected_model = None

available_models = st.session_state.gpt_manager.get_available_models()

# モデル有効性チェック
if (st.session_state.selected_model is None or 
    st.session_state.selected_model not in available_models):
    st.session_state.selected_model = available_models[0]

model = col10.selectbox(
    "モデルを選んでね",
    available_models,
    index=available_models.index(st.session_state.selected_model),
    key="model_selection"
)

# モデル変更感知処理
if st.session_state.selected_model != model:
    st.session_state.selected_model = model
    localStorage.setItem("selected_model", model)

temperature = col11.slider("会話温度（１以下推奨）", min_value=0.1, max_value=2.0, value=0.8, step=0.1)


def generate_voice(text, speed):
    params = ( #VOIVEVOX ENGINEの公式辞書機能を使うのが面倒臭くて、ここで強引に置換してます。
        ("text", text
         .replace('何でも','なんでも')
         .replace('な風に','なふうに')
        ),
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

voice_speed = col9.slider("話す速さを調整してね", min_value=0.1, max_value=2.0, value=current_speed, step=0.1)
c.execute("UPDATE girl_settings SET speed = ? where id = ?", (voice_speed, girl_settings[0]))

if st.checkbox("好きな名前をつける", value=is_custom_name):
    st.markdown(""":orange[新しい会話を始めると反映されます。 
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
if custom_info == " ": custom_info = ''

info = ''

if st.checkbox(f"カスタムキャラ設定を入力する{custom_info and '　※現在、カスタムキャラ設定が入力されています。'}"):
    st.markdown(""":orange[新しい会話を始めると反映されます。]:red[**チェックを外しても、会話中は保存されたままなので、**]  
    :orange[基本のキャラ設定に戻したい場合は、テキスト欄を空欄にしてから新しい会話を始めてください。  
    基本のキャラ設定を維持したまま、カスタムのキャラ設定を追加することもできますし、  
    基本のキャラ設定を完全に上書きし、別人にさせることもできます。  
    設定を完全上書きする場合、下のチェックボックスをチェックしてください。]""")
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
    if not check_voicevox_server():
        raise Exception("localhost:50021でVOICEVOXが起動していません。")
    chat_history = []
    with st.spinner(f"{name}が自己紹介するよ..."):
        text, api_messages = gpt_api.initBot(name, info, model, temperature)
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
        response, api_messages = gpt_api.talkBot(user_input, api_messages, model, temperature)
        return response, api_messages
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 0.6, 1, 0.5, 0.5, 0.5, 0.5])

    if col1.form_submit_button(label="送信"):
        if not check_voicevox_server():
            raise Exception("localhost:50021でVOICEVOXが起動していません。")
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
        if not check_voicevox_server():
            raise Exception("localhost:50021でVOICEVOXが起動していません。")
        with st.spinner(f"{current_chat[4]}が考えているよ..."):
            response, api_messages = gpt_api.regenerate(api_messages, model, temperature)
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

if not check_voicevox_server():
    st.warning("localhost:50021でVOICEVOXが起動していません。")

if st.session_state.selected_api == "OpenAI" and not localStorage.getItem("openai_api_key"):
    st.warning("OpenAI APIキーが見つかりませんでした。左上の⚙️メニューでAPIキーを入れて下さい。")
elif st.session_state.selected_api == "Grok" and not localStorage.getItem("grok_api_key"):
    st.warning("Grok APIキーが見つかりませんでした。左上の⚙️メニューでAPIキーを入れて下さい。")
elif st.session_state.selected_api == "Ollama" and not check_ollama_server():
    st.warning("localhost:11434でOllamaが起動していません。")

if "chat_history" in st.session_state:
    i=0
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f'<div id=chat{i}>{chat}</div>', unsafe_allow_html=True)
        params = ( #VOIVEVOX ENGINEの公式辞書機能を使うのが面倒臭くて、ここで強引に置換してます。
        ("text", chat.split('： ')[1].replace('何でも','なんでも').replace('体育倉庫','たいいくそうこ').replace('な風に','なふうに')),
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