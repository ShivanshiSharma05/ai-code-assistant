# 🤖 AI Code Assistant

### AI-Powered Repository Intelligence Platform

An intelligent developer tool that analyzes public GitHub repositories, detects risky code, evaluates complexity indicators, prioritizes files, and generates actionable recommendations for developers.

Unlike traditional AI assistants that require developers to manually paste code snippets, AI Code Assistant performs **repository-level automated analysis** and helps answer an important engineering question:

> **Which files should I fix first?**

---

## 🚀 Project Overview

Modern software repositories can contain dozens or hundreds of files. Manually reviewing every file to identify complex or risky code can be time-consuming.

AI Code Assistant automates repository analysis by:

- Fetching source files from public GitHub repositories
- Analyzing multiple files automatically
- Detecting syntax issues
- Measuring code complexity indicators
- Detecting nested loops
- Calculating code quality scores
- Assigning risk levels
- Generating risk scores
- Ranking files based on priority
- Providing actionable developer recommendations

The platform transforms raw code analysis into **Repository Intelligence**.

---

# ✨ Key Features

## 📂 GitHub Repository Analysis

Analyze public GitHub repositories using:

```text
owner/repository
```

Example:

```text
ShivanshiSharma05/ai-code-assistant-test
```

The system automatically fetches supported source files and performs multi-file analysis.

---

## 🔍 Multi-File Code Analysis

Instead of analyzing only one code snippet, the platform analyzes multiple files from a GitHub repository.

For each file, the system evaluates:

- Syntax issues
- Code complexity
- Loop count
- Nested loops
- Code quality
- Optimization opportunities
- Risk level
- Priority score

---

## 🚨 Intelligent Risk Detection

Each file is classified according to its detected complexity and quality indicators.

| Risk Level | Description |
|---|---|
| 🔴 HIGH | Complex or deeply nested logic requiring immediate attention |
| 🟠 MEDIUM | Code that should be reviewed and improved |
| 🟢 LOW | Healthy code with no immediate concerns |

The risk classification helps developers quickly identify potentially problematic files.

---

## 📊 Risk Scoring System

The platform calculates a risk score using multiple code characteristics.

Risk indicators include:

- Moderate code quality score
- High loop count
- Nested loop complexity
- Deeply nested loops
- Complex code structure

Example:

```text
complex.py

Risk Level: HIGH
Risk Score: 9
Priority Score: 9
```

---

## 🔥 Developer Priority Queue

Files are automatically ranked according to their priority score.

This helps developers answer:

> **What should I fix first?**

Instead of manually reviewing every file, developers receive a prioritized list of files requiring attention.

---

## 🎯 Developer Action Plan

The system automatically categorizes files into actionable groups.

### 🔥 Fix Immediately

Files with high-risk scores that may affect maintainability or performance.

### ⚠️ Improve Soon

Files that require review or optimization.

### ✅ Healthy Files

Files with low risk that currently require no immediate action.

---

## 📈 Repository Intelligence Dashboard

The Streamlit dashboard provides:

- Total files analyzed
- High-risk file count
- Medium-risk file count
- Low-risk file count
- Repository risk distribution
- Developer priority queue
- Developer action plan
- Detailed file analysis
- File-level recommendations

---

# 📸 Screenshots

## Repository Intelligence Dashboard

![Repository Intelligence Dashboard](screenshots/dashboard.png)

## Hard Test – Risk Detection

![Hard Test Risk Detection](screenshots/hard-test.png)

---

# 🧠 What Makes This Different From ChatGPT?

A common question is:

> **Why use this project when ChatGPT can analyze code?**

Traditional AI chat assistants generally require developers to:

1. Copy code manually
2. Paste code into the chat
3. Ask for analysis
4. Repeat the process for multiple files

AI Code Assistant automates this workflow at the repository level.

| Feature | Traditional AI Chat | AI Code Assistant |
|---|---|---|
| Analyze code snippets | ✅ | ✅ |
| Automatically fetch GitHub repositories | ❌ | ✅ |
| Analyze multiple files | Limited | ✅ |
| Repository-level analysis | ❌ | ✅ |
| Automated risk scoring | ❌ | ✅ |
| File priority ranking | ❌ | ✅ |
| Developer action plan | ❌ | ✅ |
| Repository intelligence dashboard | ❌ | ✅ |

The purpose of this project is not to replace AI assistants.

Instead, it provides a specialized engineering workflow:

```text
GitHub Repository
        ↓
Automatic Multi-File Analysis
        ↓
Complexity Detection
        ↓
Risk Scoring
        ↓
Priority Ranking
        ↓
Developer Action Plan
```

The main goal is to help developers answer:

> **Which parts of my repository require attention first?**

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │  GitHub Repository   │
                    └───────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   GitHub Service     │
                    │ Repository Fetching  │
                    └───────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │ Repository Analyzer  │
                    │ Multi-File Analysis  │
                    └───────────┬──────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
      ┌───────────────┐ ┌───────────────┐ ┌──────────────────┐
      │ Code Analyzer │ │ Risk Analyzer │ │ Repository       │
      │ Complexity    │ │ Risk Scoring  │ │ Intelligence     │
      └───────┬───────┘ └───────┬───────┘ └────────┬─────────┘
              │                 │                  │
              └─────────────────┼──────────────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    └───────────┬──────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │ Streamlit Dashboard  │
                    └──────────────────────┘
```

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- GitHub REST API

## Analysis Engine

- Python AST
- Custom Complexity Analysis
- Risk Analyzer
- Repository Intelligence Engine
- Priority Scoring Algorithm

## Frontend

- Streamlit
- Pandas
- Matplotlib

---

# 📂 Project Structure

```text
AI_Code_Assistant/
│
├── backend/
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── repositories.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── repository.py
│   │   ├── analysis.py
│   │   └── issue.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── repository_analyzer.py
│   │   ├── repository_intelligence.py
│   │   └── risk_analyzer.py
│   │
│   ├── tests/
│   │   └── __init__.py
│   │
│   ├── analyzer.py
│   ├── github_service.py
│   ├── main.py
│   ├── model.py
│   ├── create_tables.py
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── screenshots/
│   ├── dashboard.png
│   └── hard-test.png
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/ShivanshiSharma05/ai-code-assistant.git
cd ai-code-assistant
```

---

## 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file and configure your environment variables.

Example:

```env
GITHUB_TOKEN=your_github_personal_access_token
```

For backend configuration:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

⚠️ Never upload your actual `.env` file or credentials to GitHub.

Use `.env.example` files instead.

---

# ▶️ Running the Application

## Run Backend

Open a terminal:

```bash
cd backend
uvicorn main:app --reload
```

Backend server:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Run Frontend

Open another terminal:

```bash
cd frontend
streamlit run app.py
```

The Streamlit dashboard will open automatically.

---

# 🔗 API Endpoints

## Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login user |
| GET | `/auth/me` | Get current user |

---

## Repository Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/repositories/` | Get repositories |
| POST | `/repositories/` | Add repository |
| GET | `/repositories/{repository_id}` | Get repository |
| DELETE | `/repositories/{repository_id}` | Delete repository |

---

## AI Code Analysis

| Method | Endpoint | Description |
|---|---|---|
| POST | `/generate-code/` | Generate code |
| POST | `/generate-comment/` | Generate code comments |
| POST | `/generate-inline-comments/` | Generate inline comments |
| POST | `/analyze/` | Analyze code |
| POST | `/analyze-repo/` | Analyze GitHub repository |

---

# 🧪 Testing the Risk Detection System

The project was tested using files with different complexity levels.

Test files:

```text
complex.py
medium.py
simple.py
```

### Example Results

| File | Complexity | Risk Level | Priority |
|---|---|---|---|
| complex.py | O(n^k) | 🔴 HIGH | 9 |
| medium.py | O(n^k) | 🔴 HIGH | 9 |
| simple.py | O(1) | 🟢 LOW | 0 |

Example analysis output:

```json
{
  "message": "Repository analysis completed successfully",
  "summary": {
    "total_files": 3,
    "high_risk": 2,
    "medium_risk": 0,
    "low_risk": 1
  }
}
```

This demonstrates that the system can differentiate between complex and simple code structures.

---

# 📊 Example File Analysis

```json
{
  "complex.py": {
    "bugs": "No syntax errors",
    "complexity": "O(n^k)",
    "quality_score": 7,
    "risk_level": "HIGH",
    "risk_score": 9,
    "priority_score": 9,
    "line_count": 22,
    "loop_count": 5,
    "recommendation": "Fix immediately. This file has high complexity or deeply nested logic that may affect performance and maintainability."
  }
}
```

---

# 🎯 Key Innovation

The core innovation of AI Code Assistant is the combination of:

```text
Multi-File Analysis
        +
Complexity Detection
        +
Risk Scoring
        +
Priority Ranking
        +
Repository Intelligence
```

The system transforms raw analysis into an actionable developer workflow:

```text
Analyze
   ↓
Detect Risk
   ↓
Rank Files
   ↓
Recommend Action
```

Instead of simply reporting issues, the platform helps developers prioritize engineering attention.

---

# 🔮 Future Improvements

Potential future enhancements include:

- AI-powered semantic bug detection
- Code smell detection
- Security vulnerability scanning
- Pull request analysis
- GitHub Actions integration
- Automated PR recommendations
- Historical repository risk tracking
- Team-based dashboards
- Trend analysis
- Support for additional programming languages

---

# 👩‍💻 Author

**Shivanshi Sharma**

B.Tech Computer Science Engineering

Aspiring Software Engineer | Software Development | AI & Machine Learning Enthusiast

---

# ⭐ Final Takeaway

AI Code Assistant transforms traditional repository analysis:

```text
Manual Code Review
        ↓
Time Consuming
        ↓
Difficult to Prioritize
```

Into:

```text
Automated Repository Analysis
        ↓
Complexity Detection
        ↓
Risk Detection
        ↓
Priority Ranking
        ↓
Actionable Developer Plan
```

The ultimate goal is simple:

> **Help developers understand what to fix first.**