from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# load model only once
model = joblib.load("ml/saved_model/model.joblib")

@app.get("/")
def home():
    return {"message":"iris API running"}

@app.post("/predict")
def predict(data:dict):
    features = [
        [
           data["sepal_length"],
           data["sepal_width"],
           data["petal_length"],
           data["petal_width"]
        ]
    ]
    prediction = model.predict(features)
    return{"prediction":int(prediction[0])}