from dotenv import load_dotenv
load_dotenv() ##Loads all environment variables
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv("API_KEY"))

## Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_process(upload):
    if upload is not None:
        bytes_data = upload.getvalue()
        image_parts = [
            {
            "mime_type":upload.type,
            "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

##Building Streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")
st.header("Invoice Extractor")
input = st.text_input("Input Prompt: ",key = "input")
upload = st.file_uploader("Choose an invoice...",type=["jpg","jpeg","png"])
image=""
if upload is not None:
    image = Image.open(upload)
    st.image(image, caption="Uploaded Image:", use_column_width= True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices, We will upload an image as invoice and you will have to answer
questions based on the uploaded invoice image
"""

if submit:
    image_data= input_process(upload)
    response = get_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)