from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware # Yeh naya add kiya hai
import requests
import io
import os

app = FastAPI()

# 1. CORS Setup: Yeh aapki website ko connect hone dega
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Duniya ki kisi bhi website se allow karta hai
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key ko Render dashboard se automatically uthayega
REMOVE_BG_API_KEY = os.getenv("API_KEY")

@app.get("/")
def home():
    return {"message": "Nexo Backend is Running perfectly!"}

# 2. Maine route ka naam JS ke hisaab se '/remove-bg' rakha hai 
# (Toh JS mein bhi fetch link ke end mein '/remove-bg' hi rakhna)
@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    img = await file.read()
    
    res = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": img},
        headers={"X-Api-Key": REMOVE_BG_API_KEY},
        data={"size": "auto"},
    )
    
    # Agar API key galat hogi ya limit khatam hogi toh server crash nahi hoga
    if res.status_code != 200:
        return {"error": f"API Error: {res.text}"}
        
    return StreamingResponse(
        io.BytesIO(res.content),
        media_type="image/png"
    )
    
