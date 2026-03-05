from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import io
import os

app = FastAPI()

# 1. CORS Setup (Yeh perfect hai)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REMOVE_BG_API_KEY = os.getenv("API_KEY")

@app.get("/")
def home():
    return {"message": "Nexo Backend is Running perfectly!"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    img = await file.read()
    
    # YAHAN FIX KIYA HAI: Remove.bg ko file ka naam aur type batana zaroori hai
    res = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": ("image.png", img, "image/png")}, # <-- YEH LINE CHANGE HUI HAI
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
        data={"size": "auto"},
    )
    
    if res.status_code != 200:
        return {"error": f"API Error: {res.text}"}
        
    return StreamingResponse(
        io.BytesIO(res.content),
        media_type="image/png"
    )
