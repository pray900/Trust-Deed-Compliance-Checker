# embedder.py
from transformers import AutoTokenizer, AutoModel
import torch
 
MODEL_NAME = "nlpaueb/legal-bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
 
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt",
                       truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze()
    return embedding.numpy()
 
def embed_all(clauses: list):
    return [get_embedding(c) for c in clauses]