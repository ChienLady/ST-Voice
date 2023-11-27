from typing import List
import streamlit as st
import requests

from st_audiorec import st_audiorec

st.set_page_config(page_title = "Voice Demo",
    page_icon = "🔥",
    layout = "wide",
    menu_items = {
        "Get help": "https://www.facebook.com/chienlady/",
        "Report a Bug": "https://www.facebook.com/chienlady/",
        "About": "Trang web có mục đích riêng rư."
})

headers_stt = {
    "accept": "application/json",
    "Content-Type": "multipart/form-data",
}
headers_stt = {
    "accept": "application/json"
}

def main():
    endpoint = st.sidebar.text_input("Endpoint")
    
    opt = st.sidebar.selectbox("Service", ["Speech to text", "Text to speech"])
    if opt == "Speech to text":
        url = endpoint + "/stt"
        wav_audio_data = st_audiorec()
        if wav_audio_data is not None:
            with st.spinner("Processing..."):
                result = requests.post(
                    url,
                    headers = headers_stt,
                    params = {
                        "provider": "wav2vec2-nvlb"
                    },
                    files = {"file": wav_audio_data}
                )
                if result.status_code == 200:
                    result = result.json()
                    st.write(f"Output: **{result['text']}**")
                    with st.expander("Debug", False):
                        st.json(result["debug"])
                else:
                    st.error(result.status_code)
                
    else:
        url = endpoint + "/tts"
        text = st.text_area("Text", placeholder = "Viết gì đó ...")
        if st.button("Submit"):
            output = None
            with st.spinner("Fetching ..."):
                with st.expander("Process", True):
                    splits = text.split(".")
                    for split in splits:
                        audio = None
                        params = {
                            "text": split,
                            "provider": "light-speed"
                        }
                        result = requests.get(
                            url,
                            headers = headers_stt,
                            params = params,
                            stream = True
                        )
                        
                        for chunk in result.iter_content(8192):
                            if audio is None:
                                audio = chunk
                            else:
                                audio += chunk
                        if audio is not None:
                            st.write(split)
                            st.audio(audio, format = "audio/wav")
                        if output is None:
                            output = audio
                        elif isinstance(audio, bytes):
                            output += audio
            st.write("**Output**")
            st.audio(output, format = "audio/wav")
                
            
if __name__ == "__main__":
    main()

