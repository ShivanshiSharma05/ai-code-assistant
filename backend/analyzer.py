import ast

def detect_bugs(code):
    try:
        ast.parse(code)
        return "No syntax errors"
    except SyntaxError as e:
        return f"Syntax Error: {e}"


def complexity_analysis(code):
    tree = ast.parse(code)
    loops = sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))

    if loops == 0:
        return "O(1)"
    elif loops == 1:
        return "O(n)"
    elif loops == 2:
        return "O(n^2)"
    else:
        return "O(n^k)"


def code_quality(code):
    score = 10
    if len(code) > 300:
        score -= 2
    if "def " not in code:
        score -= 2
    if "#" not in code:
        score -= 2
    return max(score, 0)


def optimization_suggestions(complexity):
    if complexity == "O(n^2)":
        return "Try using sorting or binary search to improve to O(n log n)"
    elif complexity == "O(n)":
        return "Efficient. Minor optimizations possible."
    else:
        return "Optimization unclear."


def analyze_code(code):
    complexity = complexity_analysis(code)

    return {
        "bugs": detect_bugs(code),
        "complexity": complexity,
        "quality_score": code_quality(code),
        "suggestion": optimization_suggestions(complexity)
    }