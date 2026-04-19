from transformers import pipeline

# Stable small model (works on most systems)
generator = pipeline("text-generation", model="Salesforce/codegen-350M-mono")

def clean_output(text):
    lines = text.split("\n")
    clean_lines = []

    for line in lines:
        line = line.strip()

        if (
            not line or
            line.startswith("#") or
            "print(" in line and len(line) > 40
        ):
            continue

        clean_lines.append(line)

    return "\n".join(clean_lines[:15])  

def generate_code(prompt):
    formatted = f"Write a Python function for: {prompt}\n\n"

    result = generator(
        formatted,
        max_length=100,
        temperature=0.2,
        do_sample=True
    )

    output = result[0]['generated_text']

    if "def " in output:
        parts = output.split("def ")
        output = "def " + parts[1]

    if "# Driver Code" in output:
        output = output.split("# Driver Code")[0]

    return clean_output(output)

def generate_comments_inline(code):
    lines = code.split("\n")
    commented_code = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("def"):
            commented_code.append("# Function definition")
        elif stripped.startswith("for"):
            commented_code.append("# Loop to iterate")
        elif stripped.startswith("if"):
            commented_code.append("# Conditional check")
        elif "return" in stripped:
            commented_code.append("# Return result")
        elif "print" in stripped:
            commented_code.append("# Output statement")

        commented_code.append(line)

    return "\n".join(commented_code)

def generate_comment(code):
    lines = code.strip().split("\n")

    explanation = []

    for line in lines:
        line = line.strip()

        if line.startswith("for"):
            explanation.append("• A loop is used to iterate over a range of values")

        elif line.startswith("if"):
            explanation.append("• A conditional check is performed")

        elif "print" in line:
            explanation.append("• Output is printed to the console")

        elif "def" in line:
            explanation.append("• A function is defined")

    if not explanation:
        explanation.append("• The code executes sequentially line by line")

    return "\n".join(set(explanation))

    