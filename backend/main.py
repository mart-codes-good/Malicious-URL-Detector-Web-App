from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Allows frontend to speak to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # replace with frontend and backend URL's for deployment
)

# Load embedding model
embedding_model = SentenceTransformer('BAAI/bge-small-en-v1.5')

# Load random forest classifer model at startup
classifier = joblib.load("url_model_1.pkl")

class URLRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return{"status":"online"}

@app.post("/predict")
def predict(request: URLRequest):
    embedding = embedding_model.encode([request.url])  # string to num vector
    prediction = classifier.predict(embedding)          # vector to label (string)
    url_type = prediction[0]
    return{
        "url": request.url,
        "prediction": url_type
    }