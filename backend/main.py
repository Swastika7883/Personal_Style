from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session # NEW: Import Session
from utils.image_processing import analyze_image

# CHANGED: Import the database utility and model
from database import engine, get_db 
from models import Base, Outfit 
from utils.fashion_search import get_fashion_recommendations_with_db # CHANGED IMPORT

import uvicorn
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------- DATABASE INITIALIZATION -----------------
# Create tables defined in models.py (if they don't exist) when the app starts.
Base.metadata.create_all(bind=engine) 

# -----------------------------------------------------------

app = FastAPI(title="Undertone Analysis API", version="1.0.0")

origins = [
    "https://personal-style-backend.onrender.com",
    "https://personal-style-frontend.onrender.com"
]

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_undertone(
    image: UploadFile = File(...), 
    db: Session = Depends(get_db) # NEW: Inject the database session
):
    try:
        # Check if the file is an image
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Uploaded file must be an image")
        
        # Read image content
        contents = await image.read()
        
        # Analyze image
        analysis_result = analyze_image(contents)
        undertone = analysis_result["undertone"]
        
        # Get fashion recommendations, passing the database session!
        # The logic inside this function now handles the caching.
        fashion_items = get_fashion_recommendations_with_db(undertone, db)
        
        return JSONResponse({
            "undertone": undertone,
            "palette": analysis_result["palette"],
            "fashionItems": fashion_items
        })
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        # IMPORTANT: Rollback the session if an error occurs to prevent connection issues
        # (Though less critical here since the session is closed in get_db's finally block)
        if 'db' in locals():
            db.close() 
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Undertone Analysis API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)