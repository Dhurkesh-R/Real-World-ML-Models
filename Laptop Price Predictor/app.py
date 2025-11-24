import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model and DataFrame for options
pipe = pickle.load(open('laptop_price_predictor.pkl', 'rb'))
df = pickle.load(open('laptop_prices_df.pkl', 'rb'))

st.title("💻 Laptop Price Predictor")

# User Inputs
name = st.text_input('Laptop Name')

company = st.selectbox('Brand', sorted(df['Brand'].unique()))

rating = st.number_input('Rating (1.0 to 5.0)', min_value=1.0, max_value=5.0, step=0.1)

pb = st.selectbox('Processor Brand', sorted(df['Processor_brand'].unique()))

pn = st.text_input('Processor Name')

ram_gb = st.selectbox('RAM (in GB)', sorted(df['RAM_GB'].unique()))

ram_type = st.selectbox('RAM Type', sorted(df['RAM_type'].unique()))

storage_capacity = st.selectbox('Storage Capacity (in GB)', sorted(df['Storage_capacity_GB'].unique()))

storage_type = st.selectbox('Storage Type', sorted(df['Storage_type'].unique()))

graphics_name = st.text_input('Graphics Name')

graphics_brand = st.selectbox('Graphics Brand', sorted(df['Graphics_brand'].unique()))

graphics_integrated = st.selectbox('Integrated Graphics?', ['No', 'Yes'])

display_size = st.number_input('Display Size (in inches)', min_value=10.0, max_value=20.0, step=0.1)

# Get screen resolution and compute pixels
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
horizontal_pixel, vertical_pixel, ppi = 0, 0, 0

if 'x' in resolution.lower():
    try:
        horizontal_pixel, vertical_pixel = map(int, resolution.lower().split('x'))
        ppi = ((horizontal_pixel ** 2 + vertical_pixel ** 2) ** 0.5) / display_size
    except:
        st.error("Invalid resolution format. Please enter like 1920x1080.")

touch_screen = st.selectbox('Touch Screen?', ['No', 'Yes'])

os = st.selectbox('Operating System', sorted(df['Operating_system'].unique()))

# Convert 'Yes'/'No' to 1/0
touch_screen = 1 if touch_screen == 'Yes' else 0
graphics_integrated = 1 if graphics_integrated == 'Yes' else 0

# Predict button
if st.button('Predict Price'):
    input_df = pd.DataFrame([{
        'Name': name,
        'Brand': company,
        'Rating': rating,
        'Processor_brand': pb,
        'Processor_name': pn,
        'RAM_GB': ram_gb,
        'RAM_type': ram_type,
        'Storage_capacity_GB': storage_capacity,
        'Storage_type': storage_type,
        'Graphics_name': graphics_name,
        'Graphics_brand': graphics_brand,
        'Graphics_integreted': graphics_integrated,
        'Display_size_inches': display_size,
        'Horizontal_pixel': horizontal_pixel,
        'Vertical_pixel': vertical_pixel,
        'ppi': ppi,
        'Touch_screen': touch_screen,
        'Operating_system': os
    }])

    # Make prediction
    prediction = pipe.predict(input_df)[0]
    st.success(f"💰 Estimated Price: ₹{int(prediction):,}")
