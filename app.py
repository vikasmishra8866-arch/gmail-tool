import streamlit as st
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Page Settings
st.set_page_config(page_title="Bhai ka Ultimate Dashboard", page_icon="💀", layout="wide")

# ANSI Cleaning Function
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m')
    return ansi_escape.sub('', text)

# Sidebar for Navigation
st.sidebar.title("🎛️ Control Panel")
choice = st.sidebar.radio("Kaunsa Attack/Recon?", ["Email Leak Checker", "Website Recon", "API & Endpoint Finder"])

# --- TOOL 1: EMAIL LEAK CHECKER (h8mail) ---
if choice == "Email Leak Checker":
    st.title("🔍 Email Leak Checker")
    email_input = st.text_input("Enter Email to Scan:")
    if st.button("Start Hunting"):
        if email_input:
            with st.spinner('Checking database...'):
                cmd = ["h8mail", "-t", email_input, "--local"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                st.code(clean_ansi_codes(result.stdout), language="text")

# --- TOOL 2: WEBSITE RECON (Headers) ---
elif choice == "Website Recon":
    st.title("🌐 Website Intelligence")
    domain = st.text_input("Target URL (e.g., google.com):")
    if st.button("Fetch Headers"):
        if domain:
            with st.spinner('Connecting to Server...'):
                try:
                    target = f"https://{domain}" if not domain.startswith('http') else domain
                    res = requests.get(target, timeout=10)
                    st.json(dict(res.headers))
                except Exception as e:
                    st.error(f"Error: {e}")

# --- TOOL 3: API & ENDPOINT FINDER (NEW!) ---
elif choice == "API & Endpoint Finder":
    st.title("🚀 Hidden API & Endpoint Finder")
    st.write("Ye tool website ke HTML/JS mein chhupi hui API links dhundta hai.")
    target_url = st.text_input("URL daalein (e.g., https://example.com):")
    
    if st.button("Scan for Endpoints"):
        if target_url:
            with st.spinner('Scraping Source Code...'):
                try:
                    response = requests.get(target_url, timeout=15)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Pattern to find API-like strings
                    api_pattern = re.compile(r'(/[a-zA-Z0-9\._\-/]+)')
                    
                    # Finding all scripts and links
                    endpoints = set()
                    
                    # Scan Tags
                    for tag in soup.find_all(['script', 'a', 'link'], src=True):
                        endpoints.add(tag.get('src'))
                    for tag in soup.find_all(['a', 'link'], href=True):
                        endpoints.add(tag.get('href'))
                        
                    # Regex Scan in Text
                    found_paths = api_pattern.findall(response.text)
                    for path in found_paths:
                        if len(path) > 3 and ('.' in path or '/' in path):
                            endpoints.add(path)

                    st.subheader(f"Found {len(endpoints)} Potential Endpoints")
                    
                    # Filtering for interesting ones
                    api_hints = [e for e in endpoints if any(x in str(e).lower() for x in ['api', 'v1', 'json', 'graphql', 'config', 'admin'])]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.warning("🎯 Potential API/Interesting Links")
                        st.write(api_hints if api_hints else "No direct API hints found.")
                    
                    with col2:
                        st.info("📂 All Found Paths")
                        st.write(list(endpoints)[:50]) # Limiting to 50 for speed
                        
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Pehle URL toh likho!")

st.sidebar.markdown("---")
st.sidebar.caption("Built for Research | No illegal use")
