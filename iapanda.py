from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "deepseek-ai/DeepSeek-R1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")

input_text = "Bonjour, peux-tu me parler de l'IA ?"
inputs = tokenizer(input_text, return_tensors="pt").to("cuda")

output = model.generate(**inputs, max_length=200)
print(tokenizer.decode(output[0], skip_special_tokens=True))
