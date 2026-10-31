
import streamlit as st
import requests, base64, time

API_KEY = "85aedc8a7635c50bb42308bd61a42caef903248c75275a2930be3ac98d52d4ce"

st.set_page_config(page_title="Pakistan Link Checker", page_icon="🛡️")
st.title("🛡️ Pakistani Scam Link Checker")
st.write("WhatsApp wala koi bhi link yahan paste karo, mai bataungi Safe hai ya Scam!")

link = st.text_input("Link yahan paste karo:")

if st.button("Check Karo"):
    if link:
        with st.spinner("Checking... 20 sec wait"):
            headers = {"x-apikey": API_KEY}
            requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": link})
            time.sleep(20)
            url_id = base64.urlsafe_b64encode(link.encode()).decode().strip("=")
            r = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
            if r.status_code == 200:
                stats = r.json()['data']['attributes']['last_analysis_stats']
                mal = stats['malicious']
                if mal > 2:
                    st.error(f"❌ KHATRA! {mal} companies ne isko Scam kaha hai. Mat kholna!")
                else:
                    st.success(f"✅ SAFE HAI! {stats['harmless']} companies ne safe kaha.")
            else:
                st.warning("Pehli baar hai, 1 min baad dubara Check Karo button dabao")
    else:
        st.warning("Pehle link to paste karo!")
