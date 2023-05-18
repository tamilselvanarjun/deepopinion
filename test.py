import pytest
from fastapi.testclient import TestClient
from main import app
import pandas as pd
client = TestClient(app)

def test_upload_file():
    # Prepare test file
    file_path = "output.xlsx"
    # Send POST request to upload the file
    response = client.post("/fileupload", files={"file": ("output.xlsx", open(file_path, "rb"), "text/xlsx")})
    # Check response status code and content
    assert response.status_code == 200
    assert response.json() == {"status": 'Successfully uploaded'}

def test_edit_tags():
    global uploaded_df
    uploaded_df = pd.read_excel("output.xlsx")
    # Send GET request to the /home endpoint
    response = client.get("/home")
    # Check response status code
    assert response.status_code == 200
    import httpx
    assert isinstance(response, httpx.Response)
    # Clean up the uploaded data
    uploaded_df = None


def test_download_csv():
    # Send GET request to download CSV
    response = client.get("/download_csv")
    # Check response status code and headers
    assert response.status_code == 200
    assert response.headers["content-type"] == 'application/json'

def test_download_xlsx():
    # Send GET request to download CSV
    response = client.get("/download_excel")
    # Check response status code and headers
    assert response.status_code == 200
    assert response.headers["content-type"] == 'application/json'

# Add more test cases for other endpoints as needed