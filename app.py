from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚨 SABSE BADA FIX YAHAN HAI: 
# Hum 'u2netp' (Lite Model) use kar rahe hain jo sirf 4MB ka hai. 
# Isse Render ka free server kabhi crash nahi hoga!
my_session = new_session("u2netp")

@app.get("/")
def home():
    return {"message": "Nexo AI (Lite Version) is Running perfectly!"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        input_image = await file.read()
        
        # Chote AI model (session) se background remove karna
        output_image = remove(input_image, session=my_session)
        
        return Response(content=output_image, media_type="image/png")
    
    except Exception as e:
        return {"error": str(e)}
        
