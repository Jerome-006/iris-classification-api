from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"message":"iris classification API is runningd"}