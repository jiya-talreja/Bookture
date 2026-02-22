from fastapi import UploadFile,HTTPException # pyright: ignore[reportMissingImports]
max_size=15*1024*1024 #15MB max


ALLOWED_MIME_TYPES = {"application/pdf"}

async def validate_pdf(file: UploadFile) -> None:
    # 1. Check filename
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # 2. Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )

    header=await file.read(4)#read 4 bytes of data
    await file.seek(0)#use await for actually being in sync with the process and reading and going back to the bytes of actual file
    if(header!=b"%pdf"):
        return HTTPException(status_code=400,detail="The input type is not a valid type of pdf")
    file.file.seek(0,2)#reading the temp file by file.file from moving 0bytes to the very end
    size=file.file.tell()
    file.file.seek(0)
    #for max size calcualtion
    if (size>max_size):
        return HTTPException(status_code=400,detail="The size of input is more that max size")

    
