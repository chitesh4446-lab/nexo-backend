from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import requests
import io
import os

app = FastAPI()

REMOVE_BG_API_KEY = os.getenv("API_KEY")

@app.get("/")
def home():
    return {"message": "Backend Running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    img = await file.read()

    res = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": img},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
        data={"size": "auto"},
    )

    return StreamingResponse(
        io.BytesIO(res.content),
        media_type="image/png"
    )
