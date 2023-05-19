import pandas as pd
import uvicorn
import io
import json
from cachetools import cached, TTLCache
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends
import copy

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store the uploaded file data
uploaded_df = None
df = pd.DataFrame()  # Initialize an empty DataFrame

# Configure the cache with a maximum size of 100 and a time-to-live (TTL) of 600 seconds (10 minutes)
cache = TTLCache(maxsize=100, ttl=600)


@app.post("/fileupload")
async def upload_file(file: UploadFile = File(...)):
    allowed_extensions = (".csv", ".xlsx")
    ext = "." + file.filename.split(".")[-1]
    if ext.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Only CSV and XLSX files are allowed.",
        )
    global uploaded_df
    # Process the file in chunks
    CHUNK_SIZE = 1024 * 1024  # 1 MB chunk size (adjust as needed)
    content = b""
    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break
        content += chunk
    if ext.lower() == ".xlsx":
        df = pd.read_excel(io.BytesIO(content), engine="openpyxl")
    else:
        df = pd.read_csv(io.BytesIO(content))
    uploaded_df = df.copy()
    return {"status": "Successfully uploaded"}


@app.get("/home")
@cached(cache)  # Apply caching to this endpoint
def edit_tags(request: Request):
    @cached(cache)  # Apply caching to this endpoint
    def get_data():
        data = uploaded_df
        return data.to_dict("records")

    tags = get_data()
    return templates.TemplateResponse("index.html", {"request": request, "tags": tags})


@app.post("/home")
async def update_tags(request: Request):
    df = pd.DataFrame()
    form_data = await request.form()
    # text = form_data.getlist('text')
    updated_aspects = form_data.getlist("aspect")
    updated_sentiments = form_data.getlist("sentiment")
    df["text"] = uploaded_df["text"]
    df["aspect"] = updated_aspects
    df["sentiment"] = updated_sentiments
    df.to_excel("output.xlsx", index=False)
    uploaded_df = df.copy()
    return templates.TemplateResponse(
        "index.html", {"request": request, "tags": df.to_dict("records")}
    )


all_aspects = set()
all_sentiments = set()


@app.on_event("startup")
async def load_data():
    global uploaded_df, all_aspects, all_sentiments
    if uploaded_df is not None:
        all_aspects = set(uploaded_df["aspect"].unique())
        all_sentiments = set(uploaded_df["sentiment"].unique())


@app.get("/aspects")
@cached(cache)  # Apply caching to this endpoint
def get_all_aspects(aspects: set = Depends(load_data)):
    """
    Get all available aspects.
    """
    return {"aspects": list(all_aspects)}


@app.get("/sentiments")
@cached(cache)  # Apply caching to this endpoint
def get_all_sentiments(sentiments: set = Depends(load_data)):
    """
    Get all available sentiments.
    """
    return {"sentiments": list(all_sentiments)}


@app.get("/download_csv")
def download_csv():
    """
    Download the data as a CSV file.
    """
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(
            status_code=404, detail="No data available. Upload a file first."
        )
    csv_filename = "data.csv"
    uploaded_df.to_csv(csv_filename, index=False)
    return FileResponse(csv_filename, filename="data.csv", media_type="text/csv")


@app.get("/download_excel")
def download_excel():
    """
    Download the data as an Excel file (XLSX format).
    """
    global uploaded_df
    if uploaded_df is None:
        raise HTTPException(
            status_code=404, detail="No data available. Upload a file first."
        )
    excel_filename = "data.xlsx"
    uploaded_df.to_excel(excel_filename, index=False)
    return FileResponse(
        excel_filename,
        filename="data.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
