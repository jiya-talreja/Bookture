#for classifying type of pdf using fitz
import fitz # pyright: ignore[reportMissingImports]
from extraction.text_pdf import get_text
from ingestion.storeage import store_extracted_text
from typing import List
def process_pdf(file_id : str,file_path:str)->None:
    docs=fitz.open(file_path)
    text_found=False
    for page in docs:
        text=page.get_text().strip()#if file has any text not related to text_pdf file
        if text:
            text_found=True
            break
    docs.close()    
    if text_found:
        pdf_type="text_type"
        extracted_text=get_text(file_path)
        store_extracted_text(file_id,pdf_type,extracted_text)
    else:
        pdf_type="scanned-pdf"        
    print(f"for pdf id {file_id} the type is {pdf_type}")    