import azure.functions as func
import logging
import requests

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="test-container",
                               connection="BlobStorageConnectionString") 
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
