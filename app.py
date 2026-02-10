import streamlit as st
import subprocess
import re
import requests
from bs4 import BeautifulSoup

# Page Settings
st.set_page_config(page_title="Bhai ka Ultimate Dashboard", page_icon="💀", layout="wide")

# ANSI Cleaning Function
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m')
    return ansi_escape.sub('', text)

# --- SECRET SCANNER LOGIC (New!) ---
def find_secrets(text):
    # Common patterns for API Keys and Secrets
    patterns = {
        "Google API Key": r'AIza[0-9A-Za-z-_]{35}',
        "Firebase ID": r'[a-z0-9\-_]{20,}:android:[a-f0-9]+',
        "Generic Secret/Key": r'(?i)(key|api|token|secret|auth|password|pass)["\s:=>]+([0-9a-zA-Z\-_]{16,})',
        "Bearer Token": r'Bearer\s+[a-zA-Z0-9\-\._~\+\/]+=*',
        "AWS Access Key": r'AKIA[0-9A-Z]{16}'
    }
    found = []
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for m in matches:
            # Matches can be tuples if groups are used in regex
            val = m[1] if isinstance(m, tuple) else m
            found.append({"Type": name, "Value": val})
    return found

# Sidebar for Navigation
st.sidebar.title("🎛️ Control Panel")
choice = st.sidebar.radio("Kaunsa Attack/Recon?", ["Email Leak Checker", "Website Recon", "API & Secret Finder"])

fake_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# --- TOOL 1: EMAIL LEAK CHECKER ---
if choice == "Email Leak Checker":
    st.title("🔍 Email Leak Checker")
    email_input = st.text_input("Enter Email:")
    if st.button("Start Hunting"):
        if email_input:
            cmd = ["h8mail", "-t", email_input, "--local"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            st.code(clean_ansi_codes(result.stdout))

# --- TOOL 2: WEBSITE RECON ---
elif choice == "Website Recon":
    st.title("🌐 Website Intelligence")
    domain = st.text_input("Target URL:")
    if st.button("Fetch Headers"):
        try:
            target = f"https://{domain}" if not domain.startswith('http') else domain
            res = requests.get(target, headers=fake_headers, timeout=10)
            st.json(dict(res.headers))
        except Exception as e:
            st.error(f"Error: {e}")

# --- TOOL 3: API & SECRET FINDER (Updated!) ---
elif choice == "API & Secret Finder":
    st.title("🚀 Hidden API & Secret Scanner")
    target_url = st.text_input("URL daalein (e.g., https://example.com):")
    
    if st.button("Scan for Secrets"):
        if target_url:
            with st.spinner('Deep Scanning Source Code...'):
                try:
                    response = requests.get(target_url, headers=fake_headers, timeout=15)
                    
                    # 1. Find Secrets (Keys/Tokens)
                    secrets = find_secrets(response.text)
                    
                    # 2. Find Endpoints
                    soup = BeautifulSoup(response.text, 'html.parser')
                    api_pattern = re.compile(r'(/[a-zA-Z0-9\._\-/]+)')
                    endpoints = set()
                    for tag in soup.find_all(['script', 'a', 'link'], src=True):
                        endpoints.add(tag.get('src'))
                    
                    # Display Results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.error("🔑 Potential Secrets/API Keys Found")
                        if secrets:
                            st.table(secrets)
                        else:
                            st.write("No hardcoded keys found in main HTML.")
                    
                    with col2:
                        st.warning("🎯 API Hints")
                        api_hints = [e for e in endpoints if any(x in str(e).lower() for x in ['api', 'v1', 'json'])]
                        st.write(api_hints if api_hints else "No direct API hints.")
                        
                    with st.expander("All Raw Endpoints"):
                        st.write(list(endpoints))
                        
                except Exception as e:
                    st.error(f"Error: {e}")
