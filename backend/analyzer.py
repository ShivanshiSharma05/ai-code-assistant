import ast

def detect_bugs(code):
    try:
        ast.parse(code)
        return "No syntax errors"
    except SyntaxError as e:
        return f"Syntax Error: {e}"

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
        return "Try using hashing or sorting to reduce complexity"
    elif complexity == "O(n)":
        return "Consider early exit or binary search optimization"
    else:
        return "Code is already optimal"

def code_quality(code):
    score = 10

    if len(code) > 300:
        score -= 2
    if "def " not in code:
        score -= 2
    if "#" not in code:
        score -= 2

    return max(score, 0)

def analyze_code(code):
    bugs = detect_bugs(code)
    complexity = complexity_analysis(code)
    quality = code_quality(code)

    return {
        "bugs": bugs,
        "complexity": complexity,
        "quality_score": quality,
        "optimization": suggest_optimization(complexity)
    }

def project_analysis(files_dict):
    report = {}
    seen_functions = set()

    for file, code in files_dict.items():
        result = analyze_code(code)

        for line in code.split("\n"):
            if line.strip().startswith("def "):
                name = line.split("(")[0]
                if name in seen_functions:
                    result["duplication"] = "Duplicate function detected"
                else:
                    seen_functions.add(name)

        report[file] = result

    return report