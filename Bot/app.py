from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# ✅ Load fine-tuned model
MODEL_PATH = "./blenderbot-medical"
tokenizer = BlenderbotTokenizer.from_pretrained(MODEL_PATH)
model = BlenderbotForConditionalGeneration.from_pretrained(MODEL_PATH)

# ✅ System prompt (Medical chatbot instructions)
SYSTEM_PROMPT = (
    "You are a professional AI medical assistant. "
    "You provide evidence-based, factual, and reliable medical information. "
    "If the user asks about emergency situations, advise them to contact a doctor immediately. "
    "Do not provide personal diagnoses. Always remain professional and accurate."
)

# ✅ Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chatbot requests from React frontend"""
    try:
        data = request.json
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return jsonify({"reply": "Please enter a valid medical question."}), 400

        # Add system prompt before user input
        formatted_input = f"{SYSTEM_PROMPT}\nUser: {user_input}"
        
        inputs = tokenizer(formatted_input, return_tensors="pt")
        output = model.generate(**inputs)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        return jsonify({"reply": response})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": "Something went wrong on the server"}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
