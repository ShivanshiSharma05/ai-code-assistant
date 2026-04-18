import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("🚀 AI Code Assistant")

code = st.text_area("Enter Code")
prompt = st.text_input("Enter Prompt")

if st.button("Generate Code"):
    res = requests.post(f"{API}/generate-code/", params={"prompt": prompt})
    st.code(res.json()["output"])

if st.button("Generate Comment"):
    res = requests.post(f"{API}/generate-comment/", params={"code": code})
    st.write(res.json()["output"])

if st.button("Analyze Code"):
    res = requests.post(f"{API}/analyze/", params={"code": code})
    data = res.json()

    st.write("### 🐞 Bugs:", data["bugs"])
    st.write("### 📊 Complexity:", data["complexity"])
    st.write("### ⚡ Optimization:", data["optimization"])
    st.write("### ⭐ Quality Score:", data["quality_score"])

st.subheader("🔗 Analyze GitHub Repo")
repo = st.text_input("Enter repo (username/repo)")

if st.button("Analyze Repo"):
    res = requests.post(f"{API}/analyze-repo/", params={"repo_name": repo})
    st.json(res.json())