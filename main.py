from fastapi import FastAPI, File, UploadFile
import io


from fastapi.responses import StreamingResponse

from vcfReader import get_cleaned_contacts


# Create FastAPI instance
app = FastAPI()

# create an endpoint to upload VCF files

@app.post("/upload-vcf")
async def upload_file(file: UploadFile = File(...)):
    
    # read the uploaded file
    contents = await file.read()
    vcf_data = contents.decode('utf-8')

    cleaned_df = get_cleaned_contacts(vcf_data)

    stream = io.StringIO()
    cleaned_df.to_csv(stream, index=False)

    response = StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cleaned_contacts.csv"}
    )
    return response

# server check
@app.get("/")
def home():
    return {"message": "VCF Reader API is running. Go to /docs to upload."}
