from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("🔥 Loading FLAN-T5 model once...")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

print("🔥 FLAN-T5 ready!")

def get_ai_treatment(disease):

    prompt = f"""
You are an expert agriculture scientist specializing in chilli crop diseases.

Provide a detailed treatment guide for: {disease} in chilli crop.

Format your response EXACTLY as follows with these section headers:

**CAUSES:**
- List causes as bullet points

**SYMPTOMS:**
- List symptoms as bullet points

**BEST FERTILIZERS:**
- List recommended fertilizers with brief explanation

**ORGANIC TREATMENT:**
- List organic treatment methods step by step

**PREVENTION TIPS:**
- List prevention strategies as bullet points

Be specific, practical, and concise. Use only the sections listed above.
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(
        **inputs,
        max_length=512,
        min_length=50,
        repetition_penalty=2.5,
        no_repeat_ngram_size=3,
        temperature=0.7,
        do_sample=True,
        top_k=50,
        top_p=0.9
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result