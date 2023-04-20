"""Creating Hello World API"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
    Function to write Hello World
    """
    return {"message": "Hello World"}
