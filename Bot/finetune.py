import json
import torch
from datasets import load_dataset, Dataset
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration, Trainer, TrainingArguments

# ✅ Step 1: Load Data
with open("training_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Convert JSON to Hugging Face Dataset format
dataset = Dataset.from_list([{"input": d["input"], "output": d["output"]} for d in data])

# ✅ Step 2: Load Model and Tokenizer
MODEL_NAME = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(MODEL_NAME)
model = BlenderbotForConditionalGeneration.from_pretrained(MODEL_NAME)

# ✅ Step 3: Preprocess Data
def preprocess_function(examples):
    inputs = tokenizer(examples["input"], max_length=128, truncation=True, padding="max_length", return_tensors="pt")
    targets = tokenizer(examples["output"], max_length=128, truncation=True, padding="max_length", return_tensors="pt")

    return {
        "input_ids": inputs["input_ids"].squeeze(),
        "attention_mask": inputs["attention_mask"].squeeze(),
        "labels": targets["input_ids"].squeeze(),
    }

# Apply preprocessing
dataset = dataset.map(preprocess_function)
output_dir = "./blenderbot-medical"
# ✅ Step 4: Training Arguments
training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    save_strategy="epoch",  #✅ Set to "epoch" to match evaluation strategy
    evaluation_strategy="epoch",  #✅ Matches save strategy
    load_best_model_at_end=True,
    push_to_hub=False
)


# ✅ Step 5: Train Model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    eval_dataset=dataset,
    tokenizer=tokenizer
)

# Start training
trainer.train()

# ✅ Step 6: Save Fine-Tuned Model
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
