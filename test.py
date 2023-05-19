import pytest
from fastapi.testclient import TestClient
from main import app
import pandas as pd
client = TestClient(app)

#test cases should be run upon starting the server
def test_download_excel_no_data():
    # Set uploaded_df to None or empty dataframe
    uploaded_df = None
    response = client.get("/download_excel")
    # Check response status code and content
    assert response.status_code == 404
    assert response.json() == {"detail": "No data available. Upload a file first."}


def test_download_csv_no_data():
    # Set uploaded_df to None or empty dataframe
    uploaded_df = None
    response = client.get("/download_csv")
    # Check response status code and content
    assert response.status_code == 404
    assert response.json() == {"detail": "No data available. Upload a file first."}

def test_upload_excel_file():
    # Prepare test file
    global file_path
    file_path = "test.xlsx"
    # Send POST request to upload the file
    response = client.post("/fileupload", files={"file": ("output.xlsx", open(file_path, "rb"), "text/xlsx")})
    # Check response status code and content
    assert response.status_code == 200
    assert response.json() == {"status": 'Successfully uploaded'}
    

def test_upload_csv_file():
    # Prepare test file
    global file_path
    file_path = "test.csv"
    # Send POST request to upload the file
    response = client.post("/fileupload", files={"file": ("output.csv", open(file_path, "rb"), "text/csv")})
    # Check response status code and content
    assert response.status_code == 200
    assert response.json() == {"status": 'Successfully uploaded'}

def test_edit_tags():
    global uploaded_df
    uploaded_df = pd.read_csv(file_path)
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
    assert response.headers["content-type"] == 'text/csv; charset=utf-8'

def test_download_xlsx():
    # Send GET request to download CSV
    response = client.get("/download_excel")
    # Check response status code and headers
    assert response.status_code == 200
    assert response.headers["content-type"] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

# Add more test cases for other endpoints as needed

