import streamlit as st
import subprocess
import re
import requests

# Page Settings
st.set_page_config(page_title="Bhai ka Hacker Dashboard", page_icon="🛡️", layout="wide")

# ANSI Cleaning Function
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m')
    return ansi_escape.sub('', text)

# Sidebar for Navigation
st.sidebar.title("Select Tool")
choice = st.sidebar.radio("Kaunsa tool chalana hai?", ["Email Leak Checker", "Website Recon"])

# --- TOOL 1: EMAIL LEAK CHECKER (h8mail) ---
if choice == "Email Leak Checker":
    st.title("🔍 Email Leak Checker (h8mail)")
    email_input = st.text_input("Enter Email:")
    
    if st.button("Check Leak"):
        if email_input:
            with st.spinner('Checking...'):
                cmd = ["h8mail", "-t", email_input, "--local"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                clean_res = clean_ansi_codes(result.stdout)
                st.code(clean_res, language="text")
        else:
            st.warning("Email toh daalo bhai!")

# --- TOOL 2: WEBSITE RECON (Final Recon Style) ---
elif choice == "Website Recon":
    st.title("🌐 Website Recon (IP & Headers)")
    domain = st.text_input("Enter Website URL (e.g., google.com):")
    
    if st.button("Get Kundli"):
        if domain:
            with st.spinner('Fetching Data...'):
                try:
                    # Header Info nikalna
                    target = f"https://{domain}" if not domain.startswith('http') else domain
                    res = requests.get(target, timeout=10)
                    
                    st.subheader("Results for: " + domain)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("💡 Server Headers")
                        st.json(dict(res.headers))
                    
                    with col2:
                        st.success("🔒 Security Info")
                        st.write(f"Status Code: {res.status_code}")
                        st.write(f"Encoding: {res.encoding}")
                        st.write(f"Is Redirect: {res.is_redirect}")

                except Exception as e:
                    st.error(f"Error: {e}. Check if domain is valid.")
        else:
            st.warning("Domain name likho!")

st.sidebar.markdown("---")
st.sidebar.info("Tip: Website Recon se aap kisi bhi site ka server type aur security headers check kar sakte hain.")
