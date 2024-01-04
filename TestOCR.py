import streamlit as st
from os import listdir
from math import ceil
import pandas as pd
import pytesseract
from PIL import Image
import requests

def ocr_from_path(img_path):
    im = Image.open(img_path)
    im = im.convert("L") #แปลงให้เป็นภาพขาวดำ
    custom_config = r'-l tha+eng --dpi 300 --oem 3 --psm 4'  # OCR Engine Mode 3, Page Segmentation Mode 6
    text = pytesseract.image_to_string(im, config=custom_config)

    return text

def ocr_from_url(url):
    im = Image.open(requests.get(url, stream=True).raw)
    # im = Image.open(img_path)
    im = im.convert("L") #แปลงให้เป็นภาพขาวดำ
    custom_config = r'-l tha+eng --dpi 300 --oem 3 --psm 4'  # OCR Engine Mode 3, Page Segmentation Mode 6
    text = pytesseract.image_to_string(im, config=custom_config)

    return text



img_url = st.text_input('Image link')
if img_url:
    text_ocr = ocr_from_url(img_url)
    col1, col2 = st.columns(2)

    with col1:
        st.image(img_url)

    with col2:
        st.write(text_ocr)
    

    # st.write(img_url)

    # img_link  = 'https://aigencorp.com/wp-content/uploads/2021/12/ocr-a-font-sample.png.webp'
    # st.image(img_url)
    # im = Image.open(requests.get(img_link, stream=True).raw)
    # text_ocr = ocr_from_url(img_url)
    # st.image(img_url,caption=text_ocr)
    # st.write(text_ocr)

    



else:

    uploaded_files = st.file_uploader("Choose a Images file", accept_multiple_files=True,type=['png','jpeg','jpg'])


    row_size = 2
    grid = st.columns(row_size)
    col = 0
    
    for uploaded_file in uploaded_files:
        # bytes_data = uploaded_file.read()
        # st.write("filename:", uploaded_file.name)
        # st.write(bytes_data)


        if uploaded_file is not None:
            # st.image(uploaded_file)

            
            # text_ocr = ocr_from_path(uploaded_file)
            # st.write(text_ocr)


            
            with grid[col]:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)

                text_ocr = ocr_from_path(uploaded_file)
                st.image(uploaded_file, caption=text_ocr)
  
            col = (col + 1) % row_size