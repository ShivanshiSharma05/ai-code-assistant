from transformers import pipeline

generator = pipeline("text-generation", model="Salesforce/codegen-350M-mono")

def clean_output(text):
    if "Code:" in text:
        text = text.split("Code:")[-1]

    lines = list(dict.fromkeys(text.split("\n")))
    return "\n".join(lines[:10])


def generate_code(prompt):
    formatted_prompt = f"# Python code\n# {prompt}\n"

    result = generator(
        formatted_prompt,
        max_length=100,
        temperature=0.2
    )

    return clean_output(result[0]['generated_text'])


def generate_comment(code):
    formatted_prompt = f"# Explain this code:\n{code}\n# Explanation:\n"

    result = generator(
        formatted_prompt,
        max_length=100,
        temperature=0.3
    )

    return clean_output(result[0]['generated_text'])