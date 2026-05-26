from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import requests
import os

app = FastAPI()

# Allows frontend to speak to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://malicious-url-detector-web-app-6s0c.onrender.com"],
      # replace with frontend  URL's for deployment
)

# Load random forest classifer model at startup
classifier = joblib.load("url_model_1.pkl")

# Get token from .env to send a request to get model to save on ram
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/BAAI/bge-small-en-v1.5"

class URLRequest(BaseModel):
    url: str

# Route to get embedding model
def get_embedding(url: str):
    response = requests.post(
        HF_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs":url}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Embedding API failed")
    return response.json()

# Root
@app.get("/")
def root():
    return{"status":"online"}

# Route to get prediction from random forest model (benign or malicious)
@app.post("/predict")
def predict(request: URLRequest):
    embedding = get_embedding(request.url)  # string to num vector
    prediction = classifier.predict(embedding)          # vector to label (string)
    url_type = prediction[0]
    return{
        "url": request.url,
        "prediction": url_type
    }