import streamlit as st
# from os import listdir
# from math import ceil
# import pandas as pd
# import pytesseract
from PIL import Image
import requests
import easyocr
# import base64
from urllib.parse import urlparse
from io import BytesIO

def bytes_to_image(bytes_data):
    try:
        image_stream = BytesIO(bytes_data)
        image = Image.open(image_stream)
        image.save("current_img.jpg")
        
        return image
    except Exception as e:
        print("Error converting bytes to image:", e)


def ocr_easyocr(reader,path):
    result = reader.readtext(path,detail = 0)
    return '\n'.join(result)

def loadimgfromurl(url):
    # url = 'https://images.squarespace-cdn.com/content/v1/54981918e4b0bff4592d6daa/1489005122989-X3H9A1RGI08CPC1QFCST/fee.jpg?format=2500w'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save("current_img.jpg")

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
    
if 'reader' not in st.session_state:
    st.session_state.reader = easyocr.Reader(['th','en'])

img_input = st.text_input('Image URL')

if img_input:

    if is_valid_url(img_input):
        st.write('is url img')
        loadimgfromurl(img_input)
        img_input = 'current_img.jpg'

        text_ocr = ocr_easyocr(st.session_state.reader,img_input)
        col1, col2 = st.columns(2)

        with col1:
            st.image(img_input)

        with col2:
            st.write(text_ocr)

    else:
        st.write('please in put url image link')

else:

    uploaded_files = st.file_uploader("Choose a Images file", accept_multiple_files=True,type=['png','jpeg','jpg'])

    row_size = 2
    grid = st.columns(row_size)
    col = 0
    
    for uploaded_file in uploaded_files:

        if uploaded_file is not None:

            with grid[col]:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)
                bytes_to_image(bytes_data)

                text_ocr = ocr_easyocr(st.session_state.reader,'current_img.jpg')
                st.image(uploaded_file, caption=text_ocr)
  
            col = (col + 1) % row_size
    


