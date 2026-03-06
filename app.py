from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove  # <-- YEH HAI AAPKA APNA FREE AI ENGINE!

app = FastAPI()

# CORS Setup (Frontend ko block hone se rokne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Nexo 100% Free AI Backend is Running!"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # 1. Frontend se aayi photo ko read karna
        input_image = await file.read()
        
        # 2. AAPKA KHUD KA AI yahan background remove kar raha hai (No API!)
        output_image = remove(input_image)
        
        # 3. Transparent photo wapas frontend ko bhej do
        return Response(content=output_image, media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}
        
