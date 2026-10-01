import os
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Demo DevSecOps App", version="0.1.0")

@app.get("/")
def hello():
    return {
        "message": "Hello Friends, My name is Bhupender Gaur",
        "status": "active",
        "version": "0.1.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None, p: str | None = None):
    return {"item_id": item_id, "q": q, "p": p}
