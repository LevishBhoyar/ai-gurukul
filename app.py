'''
References : 
1. boto3 : https://youtu.be/JKlOlDFwsao?si=1cFFnof9HGXMfH5L
2. streamlit : https://www.youtube.com/live/YzvMpvXyUfs?si=kg2xBzNzUVrpIqxJ
3. Deploying : https://youtu.be/3sQhVKO5xAA?si=HxAnEoLj4l-OnCE5
'''


import streamlit as st
import boto3
import pandas as pd
from PIL import Image
import io

# AWS Credentials
AWS_ACCESS_KEY_ID="AKIA4JC2O7NMNX5GMF5D"
AWS_SECRET_ACCESS_KEY="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"
AWS_DEFAULT_REGION="eu-north-1"
bucket_name = "ai-gurukul-streamlit"

# Initializing the s3 client here.
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

# Trying to fetch the contents of the file.
def get_s3_file(bucket_name, file_name : str) -> None:
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    return response['Body'].read()

# Displaying if the file is fetched
def display_file(file_type : str, file_content) -> None:

    if file_type == "txt":
        st.text(file_content.decode("utf-8"))
        
    elif file_type == "csv":
        df = pd.read_csv(io.StringIO(file_content.decode("utf-8")))
        st.write(df)

    elif file_type in ["jpeg", "jpg", "png", "gif"]:
        image = Image.open(io.BytesIO(file_content))
        st.image(image, caption="Uploaded Image")
        
    else:
        st.error("Unsupported file type")



# Main Streamlit app
st.title("S3 File Viewer")

st.write("### Examples of file names you can try:")
st.write("1. `ai-gurukul.txt` - A simple text file.")
st.write("2. `waterDataset.csv` - A CSV file with sample data.")
st.write("3. `JalRakshak - SIH'24 Winners.jpg` - A JPEG image.")

# Enterend file name
file_name = st.text_input("Enter the file name in the bucket:", "ai-gurukul.txt")


# Fetching information of the entered file-name
if file_name:

    try:

        # Contents of file are fetched
        file_content = get_s3_file(bucket_name, file_name)
        file_extension = file_name.split(".")[-1].lower()

        # Processable file extensions
        if file_extension in ["txt", "csv", "jpeg", "jpg", "png", "gif"]:
            display_file(file_extension, file_content)

        # Not processable
        else:
            st.error("Unsupported file type. Please upload a text, CSV, or image file.")
    except Exception as e:
        st.error(f"Error: {e}")
