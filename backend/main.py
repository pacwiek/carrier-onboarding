import os
import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from company_classifier import classify
from company_service import get_company_data
from document_service import get_company_pdf
from krs_service import get_krs_company_data
from fastapi import UploadFile, File, Form



from verification_service import (
    save_uploaded_files,
    extract_msg_attachments,
    extract_zip_files,
    flatten_zip_folders,
    convert_images_to_pdf,
    cleanup_folder
)

from ai_service import analyze_documents

from dotenv import load_dotenv

load_dotenv()

import os


print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "ok"
    }


@app.get("/classify")
async def classify_company(
    country: str,
    tax_id: str
):
    return await classify(
        country,
        tax_id
    )


@app.get("/krs/company")
async def krs_company(
    krs: str
):
    return get_krs_company_data(
        krs
    )


@app.get("/company-data")
async def company_data(
    country: str,
    tax_id: str
):

    return await get_company_data(
        country,
        tax_id
    )


@app.get("/company-pdf")
async def company_pdf(
    country: str,
    tax_id: str
):

    result = await get_company_pdf(
        country,
        tax_id
    )

    return result


@app.get("/open-folder")
async def open_folder(
    path: str
):

    print(path)

    if os.path.isdir(path):

        subprocess.Popen(
            ["explorer", path]
        )

        return {
            "success": True
        }

    return {
        "success": False,
        "message": "Folder nie istnieje."
    }
@app.post("/verification/upload")
async def upload_verification_files(

    folder: str = Form(...),

    files: list[UploadFile] = File(...)

):

    # 1. Zapis plików
    saved = save_uploaded_files(files, folder)

    # 2. Wyciągnięcie załączników z MSG
    extract_msg_attachments(folder)

    # 3. Rozpakowanie ZIP
    extract_zip_files(folder)

    # 4. Spłaszczenie struktury katalogów
    flatten_zip_folders(folder)

    # 5. Konwersja obrazów do PDF
    convert_images_to_pdf(folder)

    # 6. Sprzątanie
    cleanup_folder(folder)

    return {

        "status": "ok",

        "files": saved

    }


@app.get("/test-ai")
def test_ai():
    return {
        "response": test_openai()
    }

@app.post("/verification/analyze")
async def analyze(folder: str = Form(...)):
    report = analyze_documents(folder)

    return {
        "report": report
    }

