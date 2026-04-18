from transformers import pipeline

generator = pipeline("text-generation", model="Salesforce/codegen-350M-mono")

cache = {}

def generate_code(prompt):
    if prompt in cache:
        return cache[prompt]

    formatted = f"# Write Python code for:\n{prompt}\n"
    result = generator(formatted, max_length=120)[0]['generated_text']
    
    cache[prompt] = result
    return result

def generate_comment(code):
    prompt = f"# Python code:\n{code}\n# Explanation:"
    result = generator(prompt, max_length=120)[0]['generated_text']
    return result