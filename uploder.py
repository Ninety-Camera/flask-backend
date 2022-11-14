import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv

load_dotenv()

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# Create a unique name for the container
image_container_name = "intrusion-images"
video_container_name = "intrusion-videos"



def upload_to_blob_storage(source_filenames,display_filenames):
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    
    image_link_list = []
  
    
    for i in range(len(source_filenames)):
        file = source_filenames[i]
        display_filename = display_filenames[i]
        blob_client = blob_service_client.get_blob_client(container=image_container_name,blob=display_filename)
    
        # create the container
        # container_client = blob_service_client.create_container(container_name)
        container_client = blob_service_client.get_container_client(image_container_name)
        with open (file,'rb') as data:
            blob_client.upload_blob(data)
        image_link_list.append('https://ninetycamera.blob.core.windows.net/'+image_container_name+'/'+display_filename)
       
    return image_link_list

def upload_video(source_filename,display_filename):
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    blob_client = blob_service_client.get_blob_client(container=video_container_name,blob=display_filename)
    container_client = blob_service_client.get_container_client(video_container_name)
    
    with open(source_filename,'rb') as data:
        blob_client.upload_blob(data)
        
    return 'https://ninetycamera.blob.core.windows.net/'+video_container_name+'/'+display_filename
            



