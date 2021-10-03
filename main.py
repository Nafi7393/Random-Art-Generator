from art_generator import generate_art
import streamlit as st
from itertools import cycle
import random


def rand_clr():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue


with st.sidebar.form(key="Image Details"):
    img_size = st.slider(label="Image Size", min_value=128, max_value=2560, value=1024)
    total_img = st.slider(label="Total How Many Images", min_value=1, max_value=20, value=1)
    st.markdown("---")

    background_clr_choice = st.radio(label="Set Background Color", options=('Random', 'Pick One'))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    background_clr = st.color_picker(label="Only if you choose 'Pick One' from above")
    st.markdown("---")

    submit = st.form_submit_button()

images = []
for i in range(total_img):
    if background_clr_choice == "Random":
        bg_clr = rand_clr()
    else:
        bg_clr = background_clr
    image = generate_art(image_size=img_size, bg_color=bg_clr)
    images.append(image)

cols = cycle(st.columns(2))
for idx, filteredImage in enumerate(images):
    next(cols).image(filteredImage, caption=f"{idx + 1}")


