import streamlit as st
import requests
import base64

API_KEY = st.secrets["API_KEY"]

st.set_page_config(page_title="Pakistani Scam Link Checker", page_icon="🛡️", layout="centered")

st.title("🛡️ Pakistani Scam Link Checker")
st.write("WhatsApp wala koi bhi link yahan check karo, 2 second mai pata chalega!")

@st.cache_data(ttl=3600, show_spinner=False)
def check_scam(link):
    try:
        url_id = base64.urlsafe_b64encode(link.encode()).decode().strip("=")
        headers = {"x-apikey": API_KEY}
        url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        r = requests.get(url, headers=headers, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

link = st.text_input("Link yahan paste karo:")

if st.button("Check Karo ⚡"):
    if not link:
        st.warning("Pehle link to paste karo!")
    else:
        with st.spinner("Checking... 2 sec wait karo ⚡"):
            result = check_scam(link)
            
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                stats = result.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                
                if malicious > 2:
                    st.error(f"⚠️ SCAM HAI! {malicious} antivirus ne dangerous bataya")
                elif malicious > 0:
                    st.warning(f"⚠️ Thora shak hai, {malicious} ne flag kia")
                else:
                    st.success("✅ Safe lag raha hai, koi scam nahi mila")
                
                with st.expander("Detail Report Dekho"):
                    st.json(stats)
