import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Code Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- STYLING ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #1f2937;
}

.chat-box {
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.user-msg {
    background-color: #2563eb;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
}

.bot-msg {
    background-color: #e5e7eb;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("💻 AI Code Assistant")
st.caption("Generate, analyze, and optimize code efficiently")

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Controls")

mode = st.sidebar.radio(
    "Select Feature",
    [
        "Code Generation",
        "Code Explanation",
        "Code Analysis",
        "GitHub Repository Analysis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("Built using AI + Static Code Analysis")

# ---------- SESSION ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- INPUT ----------
user_input = st.text_area("Enter your input", height=150)

col1, col2 = st.columns([1, 5])

with col1:
    run = st.button("Run")

# ---------- PROCESS ----------
if run and user_input.strip() != "":
    response = ""

    if mode == "Code Generation":
        res = requests.post(f"{API}/generate-code/", params={"prompt": user_input})
        response = res.json().get("output", "Error")

    elif mode == "Code Explanation":
        res = requests.post(f"{API}/generate-comment/", params={"code": user_input})
        response = res.json().get("output", "Error")

    elif mode == "Code Analysis":
        res = requests.post(f"{API}/analyze/", params={"code": user_input})
        data = res.json()

        response = f"""
🔍 **Analysis Report**

- 🐞 Bugs: {data.get("bugs")}
- 📊 Complexity: {data.get("complexity")}
- ⚡ Optimization: {data.get("optimization")}
- ⭐ Quality Score: {data.get("quality_score")}
"""

    elif mode == "GitHub Repository Analysis":
        res = requests.post(f"{API}/analyze-repo/", params={"repo_name": user_input})
        data = res.json()

        response = "📂 **Repository Analysis**\n\n"
        for file, result in data.items():
            response += f"**{file}**\n"
            response += f"- Complexity: {result.get('complexity')}\n"
            response += f"- Bugs: {result.get('bugs')}\n\n"

    # Save history
    st.session_state.history.append((user_input, response))

# ---------- OUTPUT ----------
st.markdown("## 📌 Results")

for user, bot in reversed(st.session_state.history):
    st.markdown(f"<div class='user-msg'><b>You:</b><br>{user}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='bot-msg'><b>Assistant:</b><br>{bot}</div>", unsafe_allow_html=True)