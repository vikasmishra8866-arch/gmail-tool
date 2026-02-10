import streamlit as st
import subprocess
import json

# Website ka Title aur Look
st.set_page_config(page_title="Bhai ka OSINT API", page_icon="🔍")
st.title("🔍 Email Leak Checker (h8mail)")
st.write("Apna email daalein aur dekhein ki kya aapka data leak hua hai.")

# --- API LOGIC (URL se data nikalne ke liye) ---
# Agar aap link aise use karein: ?email=test@gmail.com
query_params = st.query_params
url_email = query_params.get("email")

# User Input Box
email_input = st.text_input("Enter Email Address:", value=url_email if url_email else "")

if st.button("Check Leak") or url_email:
    if email_input:
        with st.spinner('Checking databases... Thoda sabar rakhein...'):
            try:
                # h8mail command piche se run karna
                # '--local' option se ye bina paid API ke basic leaks check karta hai
                cmd = ["h8mail", "-t", email_input, "--local"]
                result = subprocess.run(cmd, capture_output=True, text=True)

                # Output ko screen par dikhana
                st.subheader("Results:")
                if result.stdout:
                    st.code(result.stdout, language="bash")
                else:
                    st.info("Koi leak nahi mila ya tool ne respond nahi kiya.")
                
                # API Jaisa Response (JSON format mein niche dikhega)
                with st.expander("Show JSON (API Mode)"):
                    st.json({"email": email_input, "raw_data": result.stdout})

            except Exception as e:
                st.error(f"Error aagaya bhai: {e}")
    else:
        st.warning("Pehle email address toh likho!")

st.markdown("---")
st.caption("Powered by h8mail | Education Purpose Only")
