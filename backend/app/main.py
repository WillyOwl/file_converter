from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import shutil
import uuid
from tempfile import NamedTemporaryFile
from pdf2docx import Converter

app = FastAPI(title="PDF to Word Converter API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vite's default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Welcome to PDF to Word Converter API"}

@app.post("/convert")
async def convert_pdf_to_word(file: UploadFile = File(...)):
    """
    Convert PDF file to Word document.
    """
    # Check if file is PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    print(f"Received file: {file.filename}")
    
    # Generate unique filenames
    file_id = str(uuid.uuid4())
    pdf_path = os.path.join(TEMP_DIR, f"{file_id}.pdf")
    docx_path = os.path.join(TEMP_DIR, f"{file_id}.docx")
    
    try:
        # Make sure temp directory exists
        os.makedirs(TEMP_DIR, exist_ok=True)
        print(f"Saving file to: {pdf_path}")
        
        # Save uploaded PDF file
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Converting file: {pdf_path} to {docx_path}")
        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()
        
        print(f"Conversion completed. Returning file: {docx_path}")
        # Return the Word document
        return FileResponse(
            docx_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=file.filename.replace(".pdf", ".docx")
        )
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        # Clean up files in case of error
        for path in [pdf_path, docx_path]:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        # Clean up after sending the response
        file.file.close()

@app.on_event("shutdown")
def cleanup():
    """Clean up temporary files on shutdown"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)