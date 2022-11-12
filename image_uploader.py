import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

load_dotenv()

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
print(connect_str)



# Create a unique name for the container
container_name = str(uuid.uuid4())
# Create the container


def upload_to_blob_storage(source_filename,display_filename):
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    blob_client = blob_service_client.get_blob_client(container=container_name,blob=display_filename)
    
    container_client = blob_service_client.create_container(container_name)
    
    with open (source_filename,'rb') as data:
        blob_client.upload_blob(data)
    print("file uploaded.")
    
source_filename = "records/Recordcam111_11_2022_15_02_10.avi"
display_filename = "first_file"
upload_to_blob_storage(source_filename,display_filename)


