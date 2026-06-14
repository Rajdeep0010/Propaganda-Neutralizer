# imports 
import torch
import pickle
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Configuration
MODEL_DIR = r"C:\Users\boser\Desktop\Propaganda_Neutrilizer\model"
MAX_LEN = 256
device = "cude" if torch.cuda.is_available() else "cpu"

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_DIR,
    torch_dtype=torch.float32
)
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_DIR
)
model = model.to(device)
model.eval()
with open(f"{MODEL_DIR}/mlb.pkl", "rb") as f:
    mlb = pickle.load(f)

with open(f"{MODEL_DIR}/thresholds.pkl", "rb") as f:
    best_thresholds = pickle.load(f)

print(f"Model loaded | Classes: {len(mlb.classes_)} | Device: {device}")


# Detection
def detect(context, snippet):
    enc = tokenizer(
        context,
        snippet,
        max_length=MAX_LEN,
        truncation=True,
        padding='max_length',
        return_tensors="pt",
    )
    
    with torch.no_grad():
        logits = model(
            input_ids=enc["input_ids"].to(device),
            attention_mask=enc['attention_mask'].to(device)
        ).logits.float()
        
        probs = torch.sigmoid(logits).cpu().numpy()[0]

    results = sorted([
        {"technique": cls, "confidence": round(float(prob), 4)}
        for cls, prob in zip(mlb.classes_, probs)
        if prob >= best_thresholds[cls]
    ], key=lambda x: x["confidence"], reverse=True)

    return results


# Test
if __name__ == "__main__":
    context = "The radical left is destroying everything our ancestors built."
    snippet = "radical left is destroying everything"

    results = detect(context, snippet)

    print(f"\nContext  : {context}")
    print(f"Snippet  : {snippet}")
    print(f"\nDetected techniques:")
    if results:
        for r in results:
            print(f"  {r['technique']:<40} confidence: {r['confidence']:.4f}")
    else:
        print("  None detected")