from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# Load fine-tuned model
MODEL_PATH = "./blenderbot-medical"
tokenizer = BlenderbotTokenizer.from_pretrained(MODEL_PATH)
model = BlenderbotForConditionalGeneration.from_pretrained(MODEL_PATH)

def get_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    output = model.generate(**inputs)
    return tokenizer.decode(output[0], skip_special_tokens=True)

# System prompt (Medical chatbot instructions)
SYSTEM_PROMPT = (
    "You are a professional AI medical assistant. "
    "You provide evidence-based, factual, and reliable medical information. "
    "If the user asks about emergency situations, advise them to contact a doctor immediately. "
    "Do not provide personal diagnoses. Always remain professional and accurate."
)
# Test chatbot
user_input = ""
while True:
    user_input = input("Enter the Input: ")
    if user_input.lower() == "exit":
        break
    formatted_input = f"{SYSTEM_PROMPT}\nUser: {user_input}"
    print(get_response(formatted_input))
