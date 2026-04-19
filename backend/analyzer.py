import ast

def detect_bugs(code):
    try:
        ast.parse(code)
        return "No syntax errors"
    except SyntaxError as e:
        return str(e)

def complexity_analysis(code):
    loops = code.count("for") + code.count("while")

    if loops == 0:
        return "O(1)"
    elif loops == 1:
        return "O(n)"
    elif loops == 2:
        return "O(n^2)"
    else:
        return "O(n^k)"

def suggest_optimization(complexity):
    if complexity == "O(n^2)":
        return "Try using hashing or sorting to optimize"
    elif complexity == "O(n)":
        return "Consider binary search or early exit"
    return "Looks optimal"

def code_quality(code):
    score = 10

    if len(code) > 300:
        score -= 2
    if "def " not in code:
        score -= 2
    if "#" not in code:
        score -= 1

    return max(score, 1)

def analyze_code(code):
    return {
        "bugs": detect_bugs(code),
        "complexity": complexity_analysis(code),
        "optimization": suggest_optimization(complexity_analysis(code)),
        "quality_score": code_quality(code)
    }