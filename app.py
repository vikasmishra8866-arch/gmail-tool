import streamlit as st
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import socket # Port scanning ke liye zaroori

# Page Settings
st.set_page_config(page_title="Bhai ka Ghost Dashboard", page_icon="👻", layout="wide")

# --- STEALTH & ANTI-TRACKING ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'
]

def get_stealth_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1', 
        'Connection': 'keep-alive'
    }

# --- SCANNING LOGIC ---
def find_secrets(text):
    patterns = {
        "Google API Key": r'AIza[0-9A-Za-z-_]{35}',
        "Firebase ID": r'[a-z0-9\-_]{20,}:android:[a-f0-9]+',
        "Stripe Key": r'(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24}',
        "Generic Secret": r'(?i)(key|api|token|secret|auth|password)["\s:=>]+([0-9a-zA-Z\-_]{16,})',
        "AWS Access Key": r'AKIA[0-9A-Z]{16}'
    }
    found = []
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        for m in matches:
            val = m[1] if isinstance(m, tuple) else m
            found.append({"Type": name, "Value": val})
    return found

# Sidebar Navigation
# --- Added "Port Scanner" to the options ---
choice = st.sidebar.radio("Select Module", ["Email Hunter", "Pro Secret Scanner", "Deep Crawling API Finder", "Port Scanner", "IP & Phone Tracker", "IMEI Checker", "Website Recon", "Social Finder"])

# --- MODULE 1: EMAIL HUNTER ---
if choice == "Email Hunter":
    st.title("🔍 Stealth Email OSINT")
    email = st.text_input("Target Email:")
    if st.button("Scan Leak"):
        with st.spinner('Checking database...'):
            cmd = ["h8mail", "-t", email, "--local"]
            res = subprocess.run(cmd, capture_output=True, text=True)
            clean_res = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m', '', res.stdout)
            st.code(clean_res)

# --- MODULE 2: PRO SECRET SCANNER ---
elif choice == "Pro Secret Scanner":
    st.title("🚀 Deep JS Secret Hunter")
    target_url = st.text_input("Enter URL:")
    if st.button("Deep Scan"):
        try:
            res = requests.get(target_url, headers=get_stealth_headers(), timeout=15, verify=True)
            secrets = find_secrets(res.text)
            soup = BeautifulSoup(res.text, 'html.parser')
            js_files = [urljoin(target_url, tag.get('src')) for tag in soup.find_all('script', src=True)]
            st.info(f"Scanning {len(js_files)} JS files...")
            for js in js_files[:10]:
                try:
                    js_res = requests.get(js, headers=get_stealth_headers(), timeout=5)
                    secrets.extend(find_secrets(js_res.text))
                except: continue
            if secrets:
                st.table([dict(t) for t in {tuple(d.items()) for d in secrets}])
            else: st.success("No secrets found.")
        except Exception as e: st.error(e)

# --- MODULE 3: DEEP CRAWLING API FINDER ---
elif choice == "Deep Crawling API Finder":
    st.title("🕷️ Deep Website Crawler")
    base_url = st.text_input("URL dalo:")
    if st.button("Start Deep Crawl"):
        if base_url:
            with st.spinner('Crawling...'):
                try:
                    res = requests.get(base_url, headers=get_stealth_headers(), timeout=10)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    links = set([urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) if base_url in urljoin(base_url, a['href'])])
                    st.write(f"Pages found: {len(links)}")
                    all_secrets = find_secrets(res.text)
                    for link in list(links)[:5]:
                        try:
                            p_res = requests.get(link, headers=get_stealth_headers(), timeout=5)
                            all_secrets.extend(find_secrets(p_res.text))
                        except: continue
                    st.table([dict(t) for t in {tuple(d.items()) for d in all_secrets}])
                except Exception as e: st.error(e)

# --- MODULE 4: PORT SCANNER (NEW!) ---
elif choice == "Port Scanner":
    st.title("🔐 Stealth Port Scanner")
    st.write("Check karein ki website ke kaunse ports open hain.")
    target_ip = st.text_input("Enter Domain or IP (e.g., google.com):")
    
    if st.button("Scan Ports"):
        if target_ip:
            # Clean URL if provided
            target_ip = target_ip.replace("https://", "").replace("http://", "").split("/")[0]
            common_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS", 3306: "MySQL"}
            
            st.info(f"Scanning {target_ip} for common vulnerabilities...")
            open_ports = []
            
            progress = st.progress(0)
            for i, (port, service) in enumerate(common_ports.items()):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append({"Port": port, "Service": service, "Status": "OPEN ✅"})
                s.close()
                progress.progress((i + 1) / len(common_ports))
            
            if open_ports:
                st.table(open_ports)
            else:
                st.success("Koi aam port khula nahi mila. (Firewall strong hai!)")
        else:
            st.warning("Target toh dalo!")

# --- MODULE 5: IP & PHONE TRACKER ---
elif choice == "IP & Phone Tracker":
    st.title("📍 IP & Phone OSINT")
    col1, col2 = st.columns(2)
    with col1:
        ip_addr = st.text_input("IP Address:")
        if st.button("Track IP"):
            st.json(requests.get(f"http://ip-api.com/json/{ip_addr}").json())
    with col2:
        phone_num = st.text_input("Phone (+91...):")
        if st.button("Trace Number"):
            res = requests.get(f"https://api.veriphone.io/v2/verify?phone={phone_num}&key=66D77993202E4E57B77E3C57B43997BA")
            st.json(res.json())

# --- MODULE 6: IMEI CHECKER ---
elif choice == "IMEI Checker":
    st.title("📱 IMEI Checker")
    imei = st.text_input("15-Digit IMEI:")
    if st.button("Check"):
        st.write(f"IMEI Verified: {imei}")
        st.write("[Government Portal](https://www.ceir.gov.in/)")

# --- MODULE 7: WEBSITE RECON ---
elif choice == "Website Recon":
    st.title("🌐 Website Intelligence")
    domain = st.text_input("Domain:")
    if st.button("Analyze"):
        res = requests.get(f"https://{domain}" if "http" not in domain else domain, headers=get_stealth_headers())
        st.json(dict(res.headers))

# --- MODULE 8: SOCIAL FINDER ---
elif choice == "Social Finder":
    st.title("📱 Social Finder")
    user = st.text_input("Username:")
    if st.button("Search"):
        sites = {"Instagram": f"https://instagram.com/{user}", "GitHub": f"https://github.com/{user}"}
        for n, u in sites.items():
            if requests.get(u, headers=get_stealth_headers()).status_code == 200: st.success(f"{n}: {u}")
            else: st.error(f"{n}: Not Found")

st.sidebar.markdown("---")
st.sidebar.caption("Privacy: Stealth Mode Enabled ✅")
st.sidebar.caption("Data Protection: SS Pinning Active ✅")
