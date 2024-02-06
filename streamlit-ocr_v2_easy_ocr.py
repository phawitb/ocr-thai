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
import time

def reduce_image_size(byte_data, target_size_kb):
    # Open the image from byte data
    image = Image.open(BytesIO(byte_data))

    # Calculate the compression ratio needed to achieve the target size
    current_size_kb = len(byte_data) / 1024.0
    compression_ratio = target_size_kb / current_size_kb

    # Reduce the image size
    new_width = int(image.width * compression_ratio)
    new_height = int(image.height * compression_ratio)
    
    # Use Image.ANTIALIAS as a constant value for antialiasing
    resized_image = image.resize((new_width, new_height))

    # Save the resized image to a byte buffer
    output_buffer = BytesIO()
    resized_image.save(output_buffer, format='JPEG')  # You can change the format as needed (JPEG, PNG, etc.)
    output_byte_data = output_buffer.getvalue()

    return output_byte_data

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
   
    with st.spinner('load model...'):
        st.session_state.reader = easyocr.Reader(['th','en'])

img_input = st.text_input('Image URL')

if img_input:

    if is_valid_url(img_input):
        st.write('is url img')
        loadimgfromurl(img_input)
        img_input = 'current_img.jpg'

        start_time = time.time()
        with st.spinner('Wait for it...'):
            text_ocr = ocr_easyocr(st.session_state.reader,img_input)
        col1, col2 = st.columns(2)

        with col1:
            st.image(img_input)

        with col2:
            st.write(f'[{time.time()-start_time}s]{text_ocr}')

    else:
        st.write('please in put url image link')

else:

    uploaded_file = st.file_uploader("Choose a Images file", accept_multiple_files=False,type=['png','jpeg','jpg'])

    if uploaded_file:
        row_size = 2
        grid = st.columns(row_size)
        col = 0

        with grid[col]:

            bytes_data = uploaded_file.read()
            # st.write("filename:", uploaded_file.name)
            # bytes_to_image(bytes_data)

            bytes_data = reduce_image_size(bytes_data, 120)


            start_time = time.time()
            with st.spinner('Wait for it...'):
                # text_ocr = ocr_easyocr(st.session_state.reader,'current_img.jpg')
                text_ocr = ocr_easyocr(st.session_state.reader,bytes_data)

            text_ocr = f'[{time.time()-start_time}s]{text_ocr}'

            st.image(uploaded_file, caption=text_ocr)

        col = (col + 1) % row_size



    # with st.form("my-form", clear_on_submit=True):
    #     # file = st.file_uploader("FILE UPLOADER")
    #     # submitted = st.form_submit_button("UPLOAD!")

    #     # if st.button('Upload from files'):
    #     # st.write('ccc')
    #     uploaded_files = st.file_uploader("Choose a Images file", accept_multiple_files=True,type=['png','jpeg','jpg'])

    #     submitted = st.form_submit_button("UPLOAD!")

    #     row_size = 2
    #     grid = st.columns(row_size)
    #     col = 0
        
    #     for uploaded_file in uploaded_files:

    #         if uploaded_file:

    #             with grid[col]:

    #                 bytes_data = uploaded_file.read()
    #                 # st.write("filename:", uploaded_file.name)
    #                 # bytes_to_image(bytes_data)

    #                 bytes_data = reduce_image_size(bytes_data, 120)


    #                 start_time = time.time()
    #                 with st.spinner('Wait for it...'):
    #                     # text_ocr = ocr_easyocr(st.session_state.reader,'current_img.jpg')
    #                     text_ocr = ocr_easyocr(st.session_state.reader,bytes_data)

    #                 text_ocr = f'[{time.time()-start_time}s]{text_ocr}'

    #                 st.image(uploaded_file, caption=text_ocr)
    
    #             col = (col + 1) % row_size
        


