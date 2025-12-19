from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from vcfReader import get_cleaned_contacts
from datetime import datetime
from db import init_db, save_log, fetch_logs
# from api_analytics.fastapi import Analytics
import io


# Create FastAPI instance
app = FastAPI()
# app.add_middleware(Analytics, api_key = "")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    # Create database tables
    init_db()

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    # logs = fetch_logs()
    # print(f"All logs: {logs}")
    return templates.TemplateResponse("index.html", {"request": request})
# create an endpoint to upload VCF files

# data_dict = {}

@app.get("/logs", response_class=HTMLResponse)
async def serve_logs(request: Request):
    data = fetch_logs()
    return templates.TemplateResponse("logs.html", {"request": request, "logs": data})

@app.post("/upload-vcf")
async def upload_file(file: UploadFile = File(...)):
    
    # read the uploaded file
    contents = await file.read()
    vcf_data = contents.decode('utf-8')

    print(f"Received file: {file.filename}, size: {len(contents)} bytes")

    #1 timestamp of the request
    # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # data_dict["Request Time"] = now



    cleaned_df, length = get_cleaned_contacts(vcf_data)
                #2 number of rows in the uploaded file

    # data_dict["Original Contacts"] = length

    
    stream = io.StringIO()

    cleaned_df.to_csv(stream, index=False)
        #3 number of rows in the cleaned file
    
    # data_dict["Cleaned Contacts"] = len(cleaned_df)
    # print(data_dict)
    log = save_log(length, len(cleaned_df))
    print(f"Log saved with id: {log}")


    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cleaned_contacts.csv"}
    )
    return response

# # server check
# @app.get("/")
# def home():
#     return {"message": "VCF Reader API is running. Go to /docs to upload."}
