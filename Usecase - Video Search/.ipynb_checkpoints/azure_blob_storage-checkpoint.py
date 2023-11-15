import os

from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()

class BlobStorageClient:
    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        
    def create_access_container(self, container_name: str) -> ContainerClient:
        try:
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
            container_client = blob_service_client.get_container_client(container_name)
            
            if container_client.exists():
                print("Container already exists.")
                return container_client
            
            container_client.create_container()
            return container_client
        except Exception as ex:
            print('Exception:')
            print(ex)
            return None
        
    def upload_blob(self, container_client: ContainerClient, file_path: str, blob_name: str) -> BlobClient:
        try:
            blob_client = container_client.upload_blob(name=blob_name, data=file_path, overwrite=True)
            return blob_client
        except Exception as ex:
            print('Exception:')
            print(ex)
            return None
        
    def list_blobs(self, container_client: ContainerClient) -> list:
        try:
            blob_list = container_client.list_blobs()
            return list(blob_list)
        except Exception as ex:
            print('Exception:')
            print(ex)
            return None
        
    def download_blob(self, container_client: ContainerClient, blob_name: str, download_path: str) -> None:
        try:
            with open(download_path, 'wb') as download_file:
                download_file.write(container_client.download_blob(blob_name).readall())
        except Exception as ex:
            print('Exception:')
            print(ex)
            return None
        
    def delete_blob(self, container_client: ContainerClient, blob_name: str) -> None:
        try:
            container_client.delete_blob(blob_name)
        except Exception as ex:
            print('Exception:')
            print(ex)
            return None
        
    def delete_container(self, container_client: ContainerClient) -> None:
        try:
            container_client.delete_container()
        except Exception as ex:
            print('Exception:')
            print(ex)
            return None
        
if __name__ == "__main__":
    blob_storage_client = BlobStorageClient(os.getenv('AZURE_STORAGE_CONNECTION_STRING'))
    container_client = blob_storage_client.create_access_container('test-container')
    blob_client = blob_storage_client.upload_blob(container_client, 'test.txt', 'test-blob')
    # blob_list = blob_storage_client.list_blobs(container_client)
    # print(list(blob_list))
    blob_storage_client.download_blob(container_client, 'test-blob', 'download.txt')
    blob_storage_client.delete_blob(container_client, 'test-blob')
    blob_storage_client.delete_container(container_client)
