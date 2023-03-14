from io import StringIO
from typing import Union, Optional
from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import random

app = FastAPI(title="Lidio-O-Vigilante-Api666")

class CSVRequest(BaseModel):
    body: str

@app.post("/fileCsvToXlsx")
async def fileCsvToXlsx(file: Union[UploadFile, None] = None, json_data: Union[dict, None] = None):
    if json_data is not None:
        try:
            print(json_data)
            return {"csv_received": True}
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))

    elif file is not None:
        if not file.filename.endswith(".csv"):
            return { "error": "Not a csv file"}
        else:
            csv_file = pd.read_csv(file.file)
            resultadoExcel = pd.ExcelWriter(file.filename.replace(".csv", ".xlsx"), engine='xlsxwriter')
            csv_file.to_excel(resultadoExcel, index=None)
            resultadoExcel.save()

            return FileResponse(file.filename.replace(".csv", ".xlsx"))

@app.post("/jsonCsvToXlsx")
async def jsonCsvToXlsx(csv_request: CSVRequest):
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
