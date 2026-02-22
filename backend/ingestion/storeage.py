import os
import uuid
from fastapi import UploadFile # pyright: ignore[reportMissingImports]
from pathlib import Path
import json
my_dir="upload"
os.makedirs(my_dir,exist_ok=True)
async def save_pdf(file:UploadFile)->tuple[str,str]:
    file_id=str(uuid.uuid4())
    file_path=os.path.join(my_dir,f"{file_id}.pdf")#uploads/123456.pdf
    #stream to file say in chunks
    with open(file_path,"wb") as output_file:#open the filepath in write byte mode
        while True:
            chunks=await file.read(1024*1024)
            if not chunks:
                break
            output_file.write(chunks)
    await file.seek(0)
    return file_id,file_path
dir_output_text=Path("process_text")
dir_output_text.mkdir(exist_ok=True)
def store_extracted_text(file_id:str,file_type:str,extracted_text:list):
    output={
        "pdf_type":file_type,
        "pages":extracted_text
    }
    with open(dir_output_text/f"{file_id}.json","w",encoding="utf-8") as f:
        json.dump(output,f,ensure_ascii=False,indent=2)#what to write where to write if ascii-no can i read it yes
        