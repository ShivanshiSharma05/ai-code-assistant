import math

# -------------------------------
# 🔹 CLEAN OUTPUT FUNCTION
# -------------------------------
def clean_output(text):
    lines = text.split("\n")
    clean_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        clean_lines.append(line)

    return "\n".join(clean_lines[:20])


# -------------------------------
# 🔹 CODE GENERATION (LIGHTWEIGHT)
# -------------------------------
def generate_code(prompt: str):
    prompt = prompt.lower()

    if "prime" in prompt:
        code = """def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True"""

    elif "factorial" in prompt:
        code = """def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)"""

    elif "fibonacci" in prompt:
        code = """def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a)
        a, b = b, a + b"""

    elif "palindrome" in prompt:
        code = """def is_palindrome(s):
    return s == s[::-1]"""

    elif "sum of array" in prompt or "sum list" in prompt:
        code = """def array_sum(arr):
    return sum(arr)"""

    else:
        code = "# Code generation coming soon for this problem..."

    return clean_output(code)


# -------------------------------
# 🔹 CODE EXPLANATION
# -------------------------------
def generate_comment(code: str):
    lines = code.strip().split("\n")
    explanation = []

    for line in lines:
        line = line.strip()

        if line.startswith("def"):
            explanation.append("• Function is defined")

        elif line.startswith("for"):
            explanation.append("• Loop is used to iterate")

        elif line.startswith("if"):
            explanation.append("• Conditional check is applied")

        elif "return" in line:
            explanation.append("• Function returns a value")

        elif "print" in line:
            explanation.append("• Output is printed")

    if not explanation:
        explanation.append("• Code executes step by step")

    return "\n".join(set(explanation))


# -------------------------------
# 🔹 INLINE COMMENT GENERATOR
# -------------------------------
def generate_comments_inline(code: str):
    lines = code.split("\n")
    result = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("def"):
            result.append("# Function definition")

        elif stripped.startswith("for"):
            result.append("# Loop starts")

        elif stripped.startswith("if"):
            result.append("# Condition check")

        elif "return" in stripped:
            result.append("# Return statement")

        elif "print" in stripped:
            result.append("# Output statement")

        result.append(line)

    return "\n".join(result)