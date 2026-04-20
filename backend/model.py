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

        # remove unwanted junk lines
        if "###" in line:
            continue

        clean_lines.append(line)

    return "\n".join(clean_lines[:20])


# -------------------------------
# 🔹 CODE GENERATION (SMART RULE-BASED)
# -------------------------------
def generate_code(prompt: str):
    prompt = prompt.lower()

    if "reverse string" in prompt:
        code = """def reverse_string(s):
    return s[::-1]"""

    elif "prime" in prompt:
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
    sequence = []
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence"""

    elif "palindrome" in prompt:
        code = """def is_palindrome(s):
    return s == s[::-1]"""

    elif "sum of array" in prompt or "sum list" in prompt:
        code = """def array_sum(arr):
    total = 0
    for num in arr:
        total += num
    return total"""

    elif "sort" in prompt:
        code = """def sort_array(arr):
    return sorted(arr)"""

    else:
        code = """# Feature coming soon
# Try prompts like:
# - reverse string
# - prime number
# - factorial
# - fibonacci"""

    return clean_output(code)


# -------------------------------
# 🔹 CODE EXPLANATION (IMPROVED)
# -------------------------------
def generate_comment(code: str):
    lines = code.strip().split("\n")
    explanation = []

    for line in lines:
        line = line.strip()

        if line.startswith("def"):
            explanation.append("• Defines a function")

        elif line.startswith("for"):
            explanation.append("• Uses a loop for iteration")

        elif line.startswith("if"):
            explanation.append("• Applies conditional logic")

        elif "return" in line:
            explanation.append("• Returns output from function")

        elif "append" in line:
            explanation.append("• Adds elements to a list")

        elif "print" in line:
            explanation.append("• Prints output")

    if not explanation:
        explanation.append("• Code executes sequentially")

    # remove duplicates + keep order
    seen = set()
    final = []
    for item in explanation:
        if item not in seen:
            seen.add(item)
            final.append(item)

    return "\n".join(final)


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
            result.append("# Loop for iteration")

        elif stripped.startswith("if"):
            result.append("# Conditional check")

        elif "return" in stripped:
            result.append("# Returning value")

        elif "append" in stripped:
            result.append("# Adding to list")

        elif "print" in stripped:
            result.append("# Output statement")

        result.append(line)

    return "\n".join(result)