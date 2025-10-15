from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import os
from typing import List
from prometheus_fastapi_instrumentator import Instrumentator
from schemas import ReviewCreate, ReviewOut
from database import get_db, Base, engine, SessionLocal, Review  # assuming you have these

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai 
genai.configure(api_key=os.getenv("GENAI_API_KEY")) 
model = genai.GenerativeModel('gemini-2.5-flash')

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Code Review Assistant")
@app.get("/")
def read_root():
    return {"message": "Welcome to Code Reviewer API"}

@app.get("/health", summary="Health check", tags=["Monitoring"])
def health_check():
    return JSONResponse(content={"status": "ok", "uptime": "healthy"})

Instrumentator().instrument(app).expose(app)

import os
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)


import traceback
@app.post("/review", response_model=ReviewOut)
async def create_review(
    file: UploadFile = File(...),
    language: str = "python",
    db: Session = Depends(get_db)
):
    try:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file.file.seek(0)  # Ensure file pointer is at start
        code_content = (await file.read()).decode("utf-8")

        prompt = f"Review this code for readability, modularity, and potential bugs, then provide improvement suggestions.\n\n{code_content}"
        response = model.generate_content(prompt)
        review_text = response.text

        # Create DB entry
        review = Review(
            filename=file.filename,
            language=language,
            code_excerpt=code_content[:500],
            parsed_report={"suggestions": review_text},
            raw_response=str(review_text),
            created_at=datetime.utcnow()
        )
        db.add(review)
        db.commit()
        db.refresh(review)

        return review

    except Exception as e:
        print("ERROR in /review endpoint:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews", response_model=List[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).order_by(Review.created_at.desc()).all()
    return reviews

@app.get("/review/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
