from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI()

@app.post("/csv2xlsx")
async def csv2xlsx(file:UploadFile):
    if not file.filename.endswith(".csv"):
        return { "error": "Not a csv file"}

    csv_file = pd.read_csv(file.file)
    resultadoExcel = pd.ExcelWriter(file.filename.replace(".csv", ".xlsx"), engine='xlsxwriter')
    csv_file.to_excel(resultadoExcel, index=None)
    resultadoExcel.save()

    return FileResponse(file.filename.replace(".csv", ".xlsx"))
