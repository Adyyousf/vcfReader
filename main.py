from urllib import request
from fastapi import FastAPI, File, Form, UploadFile, Request
from fastapi.responses import StreamingResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from vcfReader import get_cleaned_contacts
from datetime import datetime
from db import init_db, save_log, fetch_logs, save_user, check_user
# from api_analytics.fastapi import Analytics
import io


# Create FastAPI instance
app = FastAPI()
# app.add_middleware(Analytics, api_key = "")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    # initilize database tables
    init_db()

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    # logs = fetch_logs()
    # print(f"All logs: {logs}")
    return templates.TemplateResponse("index.html", {"request": request})
# create an endpoint to upload VCF files

# data_dict = {}


@app.get("/login", response_class=HTMLResponse)
async def serve_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def process_login(
    request: Request,
    user_name: str = Form(...),
    password: str = Form(...),
    ):
    # form = await request.form()
    # user_name = form.get("user_name")
    # password = form.get("password")
    
    print(f"Received login data - Username: {user_name}, Password: {password}")

    # check user credentials in db
    status = check_user(user_name, password)
    if status == "failure":
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials. Please try again."})
    else:
        # redirect to logs page on successful login
        data = fetch_logs("SQLiteDatabases/api_requests.db")
        return templates.TemplateResponse("logs.html", {"request": request, "name": user_name, "logs": data})

    # Here, you would typically validate the user credentials against the database
    # For demonstration, we just return a success message

    # return templates.TemplateResponse("logs.html", {"request": request, "name": user_name})   

# @app.get("/logs", response_class=HTMLResponse)
# async def serve_logs(request: Request):

#     data = fetch_logs("api_requests.db")
#     return templates.TemplateResponse("logs.html", {"request": request, "logs": data})



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


@app.get("/signup", response_class=HTMLResponse)
async def serve_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
async def process_input(
    request: Request,
    name: str = Form(...),
    user_name: str = Form(...),
    password: str = Form(...),
    ):
    # form = await request.form()
    # name = form.get("name")
    # user_name = form.get("user_name")
    # password = form.get("password")

    print(f"Received signup data - Name: {name}, Username: {user_name}. Password: {password}")

    save_user(name, user_name, password)

    # Here, you would typically save the user data to the database
    # For demonstration, we just return a success message

    return templates.TemplateResponse("login.html", {"request": request, "name": name})



# log out endpoint  
@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/")
    # response = templates.TemplateResponse("index.html", {"request": request, "message": "You have been logged out successfully."})
    return response