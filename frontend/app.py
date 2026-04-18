import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("🤖 AI Code Assistant")

option = st.sidebar.selectbox(
    "Select Feature",
    ["Generate Code", "Explain Code", "Analyze Code", "Analyze GitHub Repo"]
)

if option == "Generate Code":
    prompt = st.text_area("Enter prompt")
    if st.button("Generate"):
        res = requests.post(f"{API_URL}/generate-code/", json={"prompt": prompt})
        st.code(res.json()["output"])

elif option == "Explain Code":
    code = st.text_area("Enter code")
    if st.button("Explain"):
        res = requests.post(f"{API_URL}/generate-comment/", json={"code": code})
        st.write(res.json()["output"])

elif option == "Analyze Code":
    code = st.text_area("Enter code")
    if st.button("Analyze"):
        res = requests.post(f"{API_URL}/analyze/", json={"code": code})
        st.json(res.json())

elif option == "Analyze GitHub Repo":
    repo = st.text_input("Enter GitHub repo URL")
    if st.button("Analyze Repo"):
        res = requests.post(f"{API_URL}/analyze-repo/", json={"repo_url": repo})
        st.json(res.json())