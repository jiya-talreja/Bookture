from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request,HTTPException # pyright: ignore[reportMissingImports]
from ingestion.validation import validate_pdf
from ingestion.storeage import save_pdf
from ingestion.process import process_pdf
from ingestion.storeage import store_extracted_text
from text_summary import paras_use
from pydantic import BaseModel # pyright: ignore[reportMissingImports]
from typing import List
import json
from pathlib import Path
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware # pyright: ignore[reportMissingImports]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # Step 1: Validate input
    await validate_pdf(file)
    # Step 2: Save file safely
    file_id, file_path = await save_pdf(file)
    # Step 3: Process PDF in background
    background_tasks.add_task(process_pdf, file_id, file_path)
    return {
        "job_id": file_id,
        "status": "processing_started"
    }
@app.get("/get_pro/{file_id}")
def result_text(file_id):
    file_path=Path("process_text")/f"{file_id}.json"
    if not file_path.exists():
        raise HTTPException(status_code=400,detail="Result is processing")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)       
    return data    
class PageItem(BaseModel): # pyright: ignore[reportUndefinedVariable]
    pageno: int
    paragraphs: List[str]  # pyright: ignore[reportUndefinedVariable] # or List[Any] if paragraphs can be any type

@app.post("/generate_image")
async def generate_image(page_no: PageItem):
      # <- no Request here
    print("Received page object:", page_no)
    pageno = page_no.pageno
    para=page_no.paragraphs
    answer=paras_use(page_no)
    print("ANSWER : ",answer)
    return answer
