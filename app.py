import streamlit as st
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Page Settings
st.set_page_config(page_title="Bhai ka Pro Dashboard", page_icon="🕵️‍♂️", layout="wide")

# ANSI Cleaning
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m')
    return ansi_escape.sub('', text)

# --- DEEP SECRET SCANNER LOGIC ---
def find_secrets(text):
    patterns = {
        "Google API Key": r'AIza[0-9A-Za-z-_]{35}',
        "Firebase ID": r'[a-z0-9\-_]{20,}:android:[a-f0-9]+',
        "Stripe Key": r'(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24}',
        "Generic Secret/Key": r'(?i)(key|api|token|secret|auth|password)["\s:=>]+([0-9a-zA-Z\-_]{16,})',
        "AWS Access Key": r'AKIA[0-9A-Z]{16}',
        "GitHub Token": r'ghp_[a-zA-Z0-9]{36}'
    }
    found = []
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for m in matches:
            val = m[1] if isinstance(m, tuple) else m
            found.append({"Type": name, "Value": val})
    return found

# Navigation Sidebar
st.sidebar.title("🎛️ Control Panel")
choice = st.sidebar.radio("Select Tool", ["Email Leak Checker", "Website Recon", "Pro API & JS Scanner"])

fake_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

# --- TOOLS 1 & 2 (Same as before) ---
if choice == "Email Leak Checker":
    st.title("🔍 Email Leak Checker")
    email = st.text_input("Enter Email:")
    if st.button("Scan"):
        cmd = ["h8mail", "-t", email, "--local"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        st.code(clean_ansi_codes(res.stdout))

elif choice == "Website Recon":
    st.title("🌐 Website Intelligence")
    domain = st.text_input("Target URL:")
    if st.button("Fetch"):
        try:
            target = f"https://{domain}" if not domain.startswith('http') else domain
            res = requests.get(target, headers=fake_headers, timeout=10)
            st.json(dict(res.headers))
        except Exception as e: st.error(e)

# --- TOOL 3: PRO API & JS SCANNER (DEEP SCAN) ---
elif choice == "Pro API & JS Scanner":
    st.title("🚀 Pro Hidden Secret & JS Scanner")
    st.write("Ye tool website ki saari JS files ke andar jaakar secrets dhundta hai.")
    target_url = st.text_input("URL daalein (e.g., https://spinny.com):")
    
    if st.button("Deep Scan Now"):
        if target_url:
            all_found_secrets = []
            with st.spinner('Phase 1: Scanning Main HTML...'):
                try:
                    response = requests.get(target_url, headers=fake_headers, timeout=15)
                    all_found_secrets.extend(find_secrets(response.text))
                    
                    soup = BeautifulSoup(response.text, 'html.parser')
                    js_files = [urljoin(target_url, tag.get('src')) for tag in soup.find_all('script', src=True)]
                    
                    st.info(f"Dhoond li gayi {len(js_files)} JavaScript files. Ab unke andar scan shuru...")
                    
                    # Phase 2: Scanning JS Files
                    progress_bar = st.progress(0)
                    for i, js_url in enumerate(js_files):
                        try:
                            js_res = requests.get(js_url, headers=fake_headers, timeout=10)
                            js_secrets = find_secrets(js_res.text)
                            for s in js_secrets:
                                s['Source'] = js_url.split('/')[-1] # File ka naam
                                all_found_secrets.append(s)
                        except: continue
                        progress_bar.progress((i + 1) / len(js_files))

                    # Results Display
                    st.subheader("Results Table")
                    if all_found_secrets:
                        # Duplicate remove karna
                        unique_secrets = [dict(t) for t in {tuple(d.items()) for d in all_found_secrets}]
                        st.table(unique_secrets)
                    else:
                        st.success("Koi khatarnak secret nahi mila (Ya wo bohot chhupa hua hai).")

                except Exception as e: st.error(f"Error: {e}")
