# 🤖 AI Code Assistant

An AI-powered developer tool that helps generate, explain, and analyze code using transformer models and static analysis techniques.

---

## 🚀 Features

* 💻 **Code Generation**
  Generate Python code from natural language prompts using transformer models

* 🧠 **Code Explanation**
  Automatically explain code in simple terms

* 🔍 **Bug Detection**
  Detect syntax errors using Python AST

* 📊 **Time Complexity Analysis**
  Estimate algorithm complexity (O(1), O(n), O(n²), etc.)

* ⚡ **Optimization Suggestions**
  Suggest improvements based on detected complexity

* 📁 **GitHub Repository Analysis**
  Analyze real-world repositories and evaluate code quality

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **AI Model:** Transformers (CodeGen)
* **Code Analysis:** Python AST
* **API Handling:** Requests

---

## 📂 Project Structure

```
AI_Code_Assistant/
│
├── backend/
│   ├── main.py
│   ├── model.py
│   ├── analyzer.py
│   ├── github_service.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/ai-code-assistant.git
cd ai-code-assistant
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the Project

### Start Backend

```
cd backend
uvicorn main:app --reload
```

### Start Frontend

```
streamlit run frontend/app.py
```

---

## 🌐 API Endpoints

| Endpoint             | Description                              |
| -------------------- | ---------------------------------------- |
| `/generate-code/`    | Generate code from prompt                |
| `/generate-comment/` | Explain code                             |
| `/analyze/`          | Analyze code (bugs, complexity, quality) |
| `/analyze-repo/`     | Analyze GitHub repository                |

---

## 📸 Demo (Optional)

*Add screenshots here after deployment*

---

## 🎯 Use Cases

* Developers learning coding
* Code review automation
* Quick debugging and analysis
* GitHub project evaluation

---

## 🧠 Future Improvements

* Better instruction-tuned models
* Multi-language support
* Real-time code suggestions
* Deployment with scalable APIs

---

## 👨‍💻 Author

**Shivanshi Sharma**

---

## ⭐ If you like this project

Give it a star on GitHub!
