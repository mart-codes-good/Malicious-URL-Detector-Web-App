from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Allows frontend to speak to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://malicious-url-detector-web-app-6s0c.onrender.com"],
      # replace with frontend  URL's for deployment
)

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load random forest classifer model at startup
classifier = joblib.load("url_model_1.pkl")

class URLRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return{"status":"online"}

# Route to get prediction from random forest model (benign or malicious)
@app.post("/predict")
def predict(request: URLRequest):
    embedding = embedding_model.encode([request.url])  # string to num vector
    prediction = classifier.predict(embedding)          # vector to label (string)
    url_type = prediction[0]
    return{
        "url": request.url,
        "prediction": url_type
    }