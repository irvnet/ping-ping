from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Ping-Pong App is Running"}

@app.get("/health")
def health():
    return {"message": "Ping-Ping is Healthy"}

