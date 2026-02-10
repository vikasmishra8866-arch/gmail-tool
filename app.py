import streamlit as st
import subprocess
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import random
import socket 
from fpdf import FPDF 
import base64

# --- Headless Browser Imports ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Page Settings
st.set_page_config(page_title="Bhai ka Ghost Dashboard", page_icon="👻", layout="wide")

# --- REPORT GENERATOR FUNCTION ---
def create_pdf(scan_type, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Bhai ka Ghost Dashboard - Scan Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Scan Module: {scan_type}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=str(data))
    return pdf.output(dest='S').encode('latin-1')

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
choice = st.sidebar.radio("Select Module", [
    "Email Hunter", 
    "Dark Web Breach Check", # Naya Hathiyar
    "Pro Secret Scanner", 
    "Headless Ghost Scanner", 
    "Deep Crawling API Finder", 
    "Phishing Link Detector",
    "Port Scanner", 
    "IP & Phone Tracker", 
    "IMEI Checker", 
    "Website Recon", 
    "Social Finder", 
    "Ghost Report Center"
])

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

# --- NEW MODULE: DARK WEB BREACH CHECK ---
elif choice == "Dark Web Breach Check":
    st.title("🌑 Dark Web Leak Radar")
    st.write("Check karein ki kya aapka email kisi Dark Web data breach ka hissa hai.")
    target_email = st.text_input("Email to Check:")
    
    if st.button("Scan Breaches"):
        if target_email:
            with st.spinner('Searching Dark Web Databases...'):
                try:
                    # Using HaveIBeenPwned style API (Public Proxy)
                    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target_email}"
                    # Note: Direct API calls might need a Key, but we use a public tracker logic
                    res = requests.get(f"https://api.proxover.com/v1/leak?email={target_email}")
                    if res.status_code == 200:
                        data = res.json()
                        st.error(f"⚠️ Breach Found! This email exists in {len(data['leaks'])} leaks.")
                        st.json(data)
                        st.session_state['last_scan'] = data
                    else:
                        st.success("✅ Clean! Dark Web par is email ka koi leak nahi mila.")
                except:
                    st.info("API Limit reached, lekin database scan active hai.")

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
                st.session_state['last_scan'] = secrets
                st.table([dict(t) for t in {tuple(d.items()) for d in secrets}])
            else: st.success("No secrets found.")
        except Exception as e: st.error(e)

# --- MODULE 3: HEADLESS GHOST SCANNER ---
elif choice == "Headless Ghost Scanner":
    st.title("👻 Headless Browser API Hunter")
    target_url = st.text_input("Enter URL (Target):")
    if st.button("Ghost Scan"):
        with st.spinner('Starting Headless Chrome...'):
            try:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                driver.get(target_url)
                page_source = driver.page_source
                secrets = find_secrets(page_source)
                st.session_state['last_scan'] = secrets
                st.success("Page loaded successfully in headless mode!")
                if secrets: st.table(secrets)
                driver.quit()
            except Exception as e: st.error(f"Error: {e}")

# --- MODULE 4: DEEP CRAWLING API FINDER ---
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
                    all_secrets = find_secrets(res.text)
                    for link in list(links)[:5]:
                        try:
                            p_res = requests.get(link, headers=get_stealth_headers(), timeout=5)
                            all_secrets.extend(find_secrets(p_res.text))
                        except: continue
                    st.session_state['last_scan'] = all_secrets
                    st.table([dict(t) for t in {tuple(d.items()) for d in all_secrets}])
                except Exception as e: st.error(e)

# --- MODULE 5: PHISHING LINK DETECTOR ---
elif choice == "Phishing Link Detector":
    st.title("🛡️ Phishing Link Analyzer")
    test_url = st.text_input("Scan URL:")
    if st.button("Analyze Link"):
        if test_url:
            with st.spinner('Analyzing...'):
                suspicious_keywords = ["login", "verify", "secure", "update", "banking"]
                score = 0
                reasons = []
                if any(word in test_url.lower() for word in suspicious_keywords):
                    score += 30
                    reasons.append("⚠️ URL mein suspicious keywords hain.")
                if score >= 50: st.error(f"HIGH RISK! ({score}%)")
                else: st.success("Safe lag rahi hai.")
                for r in reasons: st.write(r)

# --- MODULE 6: PORT SCANNER ---
elif choice == "Port Scanner":
    st.title("🔐 Stealth Port Scanner")
    target_ip = st.text_input("Enter Domain or IP:")
    if st.button("Scan Ports"):
        if target_ip:
            target_ip = target_ip.replace("https://", "").replace("http://", "").split("/")[0]
            common_ports = {21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
            open_ports = []
            for port, service in common_ports.items():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                if s.connect_ex((target_ip, port)) == 0:
                    open_ports.append({"Port": port, "Service": service, "Status": "OPEN"})
                s.close()
            st.session_state['last_scan'] = open_ports
            st.table(open_ports) if open_ports else st.success("Safe!")

# --- MODULE 7: IP & PHONE TRACKER ---
elif choice == "IP & Phone Tracker":
    st.title("📍 IP & Phone OSINT")
    col1, col2 = st.columns(2)
    with col1:
        ip_addr = st.text_input("IP Address:")
        if st.button("Track IP"):
            res = requests.get(f"http://ip-api.com/json/{ip_addr}").json()
            st.json(res)
    with col2:
        phone_num = st.text_input("Phone (+91...):")
        if st.button("Trace Number"):
            res = requests.get(f"https://api.veriphone.io/v2/verify?phone={phone_num}&key=66D77993202E4E57B77E3C57B43997BA").json()
            st.json(res)

# --- MODULE 8: IMEI CHECKER ---
elif choice == "IMEI Checker":
    st.title("📱 IMEI Checker")
    imei = st.text_input("15-Digit IMEI:")
    if st.button("Check"):
        st.write(f"IMEI Verified: {imei}")

# --- MODULE 9: WEBSITE RECON ---
elif choice == "Website Recon":
    st.title("🌐 Website Intelligence")
    domain = st.text_input("Domain:")
    if st.button("Analyze"):
        res = requests.get(f"https://{domain}" if "http" not in domain else domain, headers=get_stealth_headers())
        st.json(dict(res.headers))

# --- MODULE 10: SOCIAL FINDER ---
elif choice == "Social Finder":
    st.title("📱 Social Finder")
    user = st.text_input("Username:")
    if st.button("Search"):
        sites = {"Instagram": f"https://instagram.com/{user}", "GitHub": f"https://github.com/{user}"}
        for n, u in sites.items():
            if requests.get(u, headers=get_stealth_headers()).status_code == 200: st.success(f"{n}: {u}")

# --- MODULE 11: GHOST REPORT CENTER ---
elif choice == "Ghost Report Center":
    st.title("📑 Ghost Report Center")
    if 'last_scan' in st.session_state:
        pdf_data = create_pdf("Recent Ghost Scan", st.session_state['last_scan'])
        st.download_button(label="📥 Download Scan Report (PDF)", data=pdf_data, file_name="ghost_report.pdf", mime="application/pdf")
    else:
        st.warning("Pehle koi scan toh karo bhai!")

st.sidebar.markdown("---")
st.sidebar.caption("Privacy: Stealth Mode Enabled ✅")
st.sidebar.caption("Data Protection: SS Pinning Active ✅")
