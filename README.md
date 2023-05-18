Deepopinion

This project allows user to upload the files of training data for ML model and label it. Also user has able to download the data from api post uploading.

This project is implemented user FastAPI() framework. Below is the list of available API's:

![image](https://github.com/arjunlimat/deepopinion/assets/42732673/aa1d53ae-c627-4b2c-9f8a-76f622cfeb0f)

 

Sample User Upload File:
As per the given JSON request for single input text can have more than 1 tag. So Below is the sample user upload file 
 

http://127.0.0.1:8000/fileupload
Takes .xlsx or .csv file as input and store that into the local drive. But this can be changed and inserted into the database. Incase file size is large this will be processed as chunk by chunk in the code. This is handled in code.

![image](https://github.com/arjunlimat/deepopinion/assets/42732673/a9ad4fd1-4c1e-425f-8c79-26b3400d63fd)


http://127.0.0.1:8000/home
This will display the list of data that the user has uploaded. Users can able to change a tag
by changing either the aspect or a sentiment (or both). Upon clicking on Submit button these data will be stored in the local drive. 

 ![image](https://github.com/arjunlimat/deepopinion/assets/42732673/188dd8e4-54be-48c4-923d-fd35909348dd)


http://127.0.0.1:8000/aspects
It will fetch the all unique aspects from the file. Once we integrate with the database it will be fetched from the database.
http://127.0.0.1:8000/sentiments
It will fetch the all unique sentiments from the file. Once we integrate with the database it will be fetched from the database.

http://127.0.0.1:8000/download_csv
It will download the data and put that into CSV file

http://127.0.0.1:8000/sentiments
It will download the data and put that into XLSX file

Considerations:

When dealing with large files and the need for caching to improve latency and throughput, a Python framework like Django or Flask can be suitable. However, considering the specific requirements, The input files can be very big (more than 1 GB). Having a solution that handles such large files is a plus. handling large files efficiently might require additional considerations. In such cases, a framework like FastAPI can be a good choice. Here's why:

Performance: FastAPI is built on top of Starlette, an asynchronous web framework. Its async capabilities allow for handling multiple requests concurrently, resulting in higher performance and better scalability compared to the synchronous nature of Django and Flask. This is particularly beneficial when implementing caching, as it enables efficient utilization of caching mechanisms and reduces latency.

Make sure to not block the API

FastAPI fully supports the asyncio library, which enables non-blocking and asynchronous operations. This allows you to efficiently handle large file uploads and downloads without blocking other requests or causing performance issues. You can leverage the asyncio framework and its libraries, such as aiofiles or aiohttp, to handle file operations asynchronously.

Upon file uploading the file and the remaining api's will start to work. Because we need to initial data that is coming file upload api.
Also we can integrate this with Database and show the values from the database as next step. 

To start the uvicorn server please run python main.py in terminal. it will start the local server http://127.0.0.1:8000/

















