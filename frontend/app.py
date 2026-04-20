import streamlit as st
import requests

API = "https://ai-code-assistant-f1lw.onrender.com"

st.set_page_config(page_title="AI Code Assistant", layout="wide")

st.title("💻 AI Code Assistant")

mode = st.sidebar.selectbox(
    "Select Feature",
    ["Code Generation", "Code Explanation", "Code Analysis", "GitHub Analysis", "Code Comment Generator"]
)

user_input = st.text_area("Enter input")

if st.button("Run"):
    if mode == "Code Generation":
        res = requests.post(f"{API}/generate-code/", json={"prompt": user_input})
        data = res.json()

        if "output" in data:
          st.code(data["output"])
        elif "error" in data:
          st.error(data["error"])
        else:
          st.write(data)

    elif mode == "Code Explanation":
        res = requests.post(f"{API}/generate-comment/", json={"code": user_input})
        st.write(res.json()["output"])
        

    elif mode == "Code Analysis":
        res = requests.post(f"{API}/analyze/", json={"code": user_input})
        data = res.json()
        

        st.write("### Bugs:", data["bugs"])
        st.write("### Complexity:", data["complexity"])
        st.write("### Optimization:", data["optimization"])
        st.write("### Quality Score:", data["quality_score"])

    elif mode == "GitHub Analysis":
        res = requests.post(f"{API}/analyze-repo/", json={"repo": user_input})
        st.json(res.json())

    elif mode == "Code Comment Generator":
        res = requests.post(
            f"{API}/generate-inline-comments/",
            json={"code": user_input}
    )
    st.code(res.json()["output"])    