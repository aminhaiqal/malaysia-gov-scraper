from transformers import AutoTokenizer, AutoModel
import torch

MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"

# Load model & tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)
model.eval()

def embed_text(text: str):
    """
    Generate 0.6B embedding vector for a text using Qwen3
    """
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=2048)
        outputs = model(**inputs)
        # outputs.embeddings might vary depending on Qwen implementation
        embedding = outputs[0][0].to("cpu").numpy()
    return embedding.tolist()
