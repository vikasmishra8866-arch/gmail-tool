import streamlit as st
import subprocess
import re

# Website ka Title
st.set_page_config(page_title="Bhai ka OSINT API", page_icon="🔍")
st.title("🔍 Email Leak Checker (h8mail)")
st.write("Apna email daalein aur dekhein ki kya aapka data leak hua hai.")

# URL se data nikalne ke liye API logic
query_params = st.query_params
url_email = query_params.get("email")

# User Input Box
email_input = st.text_input("Enter Email Address:", value=url_email if url_email else "")

# ANSI Codes hatane ke liye function (Cleaning Logic)
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\d+m')
    return ansi_escape.sub('', text)

if st.button("Check Leak") or url_email:
    if email_input:
        with st.spinner('Checking databases... Thoda sabar rakhein...'):
            try:
                # h8mail command run karna
                cmd = ["h8mail", "-t", email_input, "--local"]
                result = subprocess.run(cmd, capture_output=True, text=True)

                # Output ko saaf karna
                raw_output = result.stdout
                clean_output = clean_ansi_codes(raw_output)

                st.subheader("Results:")
                if clean_output.strip():
                    # Saaf sutra output dikhana
                    st.code(clean_output, language="text")
                else:
                    st.info("Koi leak nahi mila ya tool ne respond nahi kiya.")
                
                # API Jaisa Response (JSON)
                with st.expander("Show JSON (API Mode)"):
                    st.json({"email": email_input, "data": clean_output})

            except Exception as e:
                st.error(f"Error aagaya bhai: {e}")
    else:
        st.warning("Pehle email address toh likho!")

st.markdown("---")
st.caption("Powered by h8mail | Clean Version")
