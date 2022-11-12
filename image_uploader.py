import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

load_dotenv()

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Create a unique name for the container
container_name = "intrusion-images"




def upload_to_blob_storage(source_filenames,display_filenames):
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    
    image_link_list = []
  
    
    for i in range(len(source_filenames)):
        file = source_filenames[i]
        display_filename = display_filenames[i]
        blob_client = blob_service_client.get_blob_client(container=container_name,blob=display_filename)
    
        # create the container
        # container_client = blob_service_client.create_container(container_name)
        container_client = blob_service_client.get_container_client(container_name)
        with open (file,'rb') as data:
            blob_client.upload_blob(data)
        image_link_list.append('https://ninetycamera.blob.core.windows.net/'+container_name+'/'+display_filename)
       
    return image_link_list
    
    
def get_blob(container_name,blob_name):
        blob = BlobClient.from_connection_string(connect_str, container_name, blob_name)
        with open("./BlockDestination.avi", "wb") as my_blob:
            blob_data = blob.download_blob()
            blob_data.readinto(my_blob)
            



