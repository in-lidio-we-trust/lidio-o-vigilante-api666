from io import StringIO
from typing import Union, Optional
from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Header
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import random
import io

TOKEN_FILE = "token.txt"

app = FastAPI(title="Lidio-O-Vigilante-Api666")


def authenticate(token: str):
    with open(TOKEN_FILE, "r") as f:
        saved_token = f.read().strip()
        if token == saved_token:
            return True
    return False

class CSVRequest(BaseModel):
    body: str

@app.post("/fileCsvToXlsx")
async def fileCsvToXlsx(file:UploadFile, token: str = Header(None)):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    if not file.filename.endswith(".csv"):
        return { "error": "Not a csv file"}

    csv_file = pd.read_csv(file.file)
    resultadoExcel = pd.ExcelWriter(file.filename.replace(".csv", ".xlsx"), engine='xlsxwriter')
    csv_file.to_excel(resultadoExcel, index=None)
    resultadoExcel.save()

    return FileResponse(file.filename.replace(".csv", ".xlsx"))

@app.post("/jsonCsvToXlsx")
async def jsonCsvToXlsx(csv_request: CSVRequest, token: str = Header(None)):
    if not authenticate(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        csvString = csv_request.body
        csvStringIO = StringIO(csvString)
        csv_file = pd.read_csv(csvStringIO)
        filename = 'Roi'+ str(random.randint(100000000, 999999999)) + ".xlsx"
        resultadoExcel = pd.ExcelWriter(filename, engine='xlsxwriter')
        csv_file.to_excel(resultadoExcel, index=None)
        resultadoExcel.save()
        return FileResponse(filename)


    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
