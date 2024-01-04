# import streamlit as st 

# st.header("Hello World 👏")

# st.image('imgs/191984.jpg', use_column_width = 'auto' ,caption='Sunrise by the mountains')



import streamlit as st
from os import listdir
from math import ceil
import pandas as pd
import pytesseract
from PIL import Image


st.set_page_config(layout="wide")

def ocr(img_path):
    im = Image.open(img_path)
    im = im.convert("L") #แปลงให้เป็นภาพขาวดำ
    custom_config = r'-l tha+eng --dpi 300 --oem 3 --psm 4'  # OCR Engine Mode 3, Page Segmentation Mode 6
    text = pytesseract.image_to_string(im, config=custom_config)

    return text


directory = r'images/ocr'
files = listdir(directory)

def initialize():    
    df = pd.DataFrame({'file':files,
                    'incorrect':[False]*len(files),
                    'label':['']*len(files)})
    df.set_index('file', inplace=True)
    return df

if 'df' not in st.session_state:
    df = initialize()
    st.session_state.df = df
else:
    df = st.session_state.df 


controls = st.columns(3)
with controls[0]:
    batch_size = st.select_slider("images/page:",range(10,110,10),value = 20)
with controls[1]:
    row_size = st.select_slider("Row size:", range(1,6), value = 3)
num_batches = ceil(len(files)/batch_size)
with controls[2]:
    page = st.selectbox("Page", range(1,num_batches+1))


def update (image, col): 
    df.at[image,col] = st.session_state[f'{col}_{image}']
    if st.session_state[f'incorrect_{image}'] == False:
       st.session_state[f'label_{image}'] = ''
       df.at[image,'label'] = ''

batch = files[(page-1)*batch_size : page*batch_size]

grid = st.columns(row_size)
col = 0
for image in batch:
    with grid[col]:

        img_path = f'{directory}/{image}'
        caption = ocr(img_path)

        st.image(img_path, caption=caption)
        # st.checkbox("Incorrect", key=f'incorrect_{image}', 
        #             value = df.at[image,'incorrect'], 
        #             on_change=update, args=(image,'incorrect'))
        # if df.at[image,'incorrect']:
        #     st.text_input('New label:', key=f'label_{image}', 
        #                   value = df.at[image,'label'],
        #                   on_change=update, args=(image,'label'))
        # else:
        #     st.write('##')
        #     st.write('##')
        #     st.write('###')
    col = (col + 1) % row_size

# st.write('## Corrections')
# df[df['incorrect']==True]