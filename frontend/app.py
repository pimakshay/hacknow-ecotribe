import io
import os

import requests
import streamlit as st
from azure.storage.blob import BlobServiceClient
from langchain_openai import AzureChatOpenAI
from PIL import Image

# Azure Blob Storage Configuration
#AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=ecotribe;AccountKey=G7HKdQ2xSh0aXLBA+ybiLOaPvruVPr+RvQyIjjGtYRFFUet/WOGKIAnQl/xD3Mxzlewp0hpTQVCj+AStp/A7vg==;EndpointSuffix=core.windows.net"
#CONTAINER_NAME = "ecotribe-container"

# Azure OpenAI API Configuration
#AZURE_OPENAI_ENDPOINT = "https://eco-tribe-ai.openai.azure.com/openai/deployments/general-task-model/chat/completions?api-version=2023-03-15-preview"
#AZURE_OPENAI_API_KEY = "97b85527db474f2386c3633e54702f76"

        
llm = AzureChatOpenAI(
    api_key="b36879e47f2d42109a3d54edb22f78c3",
    azure_endpoint="https://ecotribe.openai.azure.com/openai/deployments/Chat/chat/completions?api-version=2024-02-15-preview",
    api_version="2024-02-15-preview",
    model="gpt-4o-2024-08-06",
    temperature=0,
    max_tokens=None,
)

import base64

from langchain_core.prompts import ChatPromptTemplate


# Function to resize the image to reduce size
def resize_image(uploaded_file, max_width, max_height):
    # Open the image using PIL
    image = Image.open(uploaded_file)

    # Calculate the aspect ratio to resize without distorting
    image.thumbnail((max_width, max_height))

    # Save the resized image to a BytesIO object
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    
    # Return the resized image bytes
    img_byte_arr.seek(0)
    return img_byte_arr


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image(image_path):
    image_base64 = image_to_base64(image_path)
    prompt = ChatPromptTemplate.from_messages([
                ("system", '''You are an expert at detecting the type of fruits, and their qualities from an input image. These qualities include color, and surface texture. You also identify if there is any mold, and if the fruit is defective.
            The input images can include images of fresh, semi-ripen, fully-ripen, or rotten fruits.
            Your task is to return a json object with following keys:
            {{
            "object_name": str, # name of the fruit
            "color": str, # color of the fruit
            "surface_texture": str, # texture of the surface: ["smooth", "rough", "fuzzy", "wrinkled", "bumpy", "waxy", "spiky", "dimpled"] 
            "has_mold_spot": str, # yes or no
            "shape": str # options: ["normal", "distorted", "swollen", "shriveled"]
            }}
        
        These information would help the user to identify if the fruit is fresh, partially-ripen, fully-ripen, partially-rotten, or fully-roten.
        '''),
        ("human", "Please analyze this fruit image and return JSON object as mentioned in the instructions."),
        ("human", f"![fruit_image](data:image/jpeg;base64,{image_base64})")
    ])
    # output_parser = JsonOutputParser()
    response = llm.invoke(prompt.format(), response_format={"type": "json_object"})
    print(response)
    return response

def main():
    sidebar = st.sidebar

    # set 'wide' as the default page layout
    st.set_page_config(layout="wide")
    sidebar.title("Parameters")

    # set the title without using bold font and by using white and make it left aligned
    st.markdown("<h2 style='text-align: left; color: black;'>AI Pipeline</h2>", unsafe_allow_html=True)

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Add a title on top of each separation line, describing the content of each column
    with col1:
        st.markdown("<h3 style='text-align: center;'>Uploaded Image</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3 style='text-align: center;'>Intermediate Results</h3>", unsafe_allow_html=True)
    with col3:
        st.markdown("<h3 style='text-align: center;'>Call-To-Action</h3>", unsafe_allow_html=True)

    # add thin separation line in streamlit for each column
    col1.markdown("---")
    col2.markdown("---")
    col3.markdown("---")

    # Step 1: Upload the image
    uploaded_file = sidebar.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])
    
    # print the filepath of uploaded_file
    
    if uploaded_file is not None:
        with col1:
            # Display the uploaded image on the left side
            st.image(Image.open(uploaded_file), use_column_width=True)

        # Step 2: Create a button in the right column to run Azure AI
        with col2:
            # locate the button centered in the sidebar

            upload_dir = "uploaded_files"
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.write("File path:", file_path)

            if sidebar.button("Run Pipeline"):
                response = analyze_image(file_path)
                st.write(response)

if __name__ == "__main__":
    main()
