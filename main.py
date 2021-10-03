from art_generator import generate_art
import streamlit as st
from itertools import cycle
import random

st.set_page_config(page_title="Random Art Generator")


def rand_clr():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


option = ["Horizontal", "Vertical", "Random Shape"]
all_effects = ["lighter".upper(), "difference".upper(), "screen".upper(), "add".upper(), "subtract".upper()]

with st.sidebar.form(key="Image Details"):
    img_option = st.selectbox(label="What type of image you want?", options=option)
    img_size = st.slider(label="Image Size", min_value=128, max_value=3450, value=1024)
    total_lines_in_img = st.slider(label="Total Number of Lines", min_value=5, max_value=50, value=10)
    total_img = st.slider(label="Total How Many Images", min_value=1, max_value=20, value=1)
    st.markdown("---")

    background_clr_choice = st.radio(label="Set Background Color", options=('Random', 'Pick One'))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    background_clr = st.color_picker(label="Only if you choose 'Pick One' from above")
    st.markdown("---")

    line_clr_choice = st.radio(label="Set Line Color", options=('Random', 'Pick One'))
    st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
    st.write('<p style="font-size: 13.5px;">Only if you choose "Pick One" from above</p>', unsafe_allow_html=True)
    start_clr = hex_to_rgb(st.color_picker(label="Line Start Color"))
    end_clr = hex_to_rgb(st.color_picker(label="Line End Color"))
    st.markdown("---")

    effect_option = st.selectbox(label="What type of image you want?", options=all_effects, index=0)

    submit = st.form_submit_button()

images = []
cols = cycle(st.columns(2))
st.write(cols)

if img_option == option[0]:
    horizontal = True
    vertical = False
elif img_option == option[1]:
    horizontal = False
    vertical = True
else:
    horizontal = False
    vertical = False

for i in range(total_img):
    if background_clr_choice == "Random":
        bg_clr = rand_clr()
    else:
        bg_clr = background_clr

    if line_clr_choice != "Pick One":
        image = generate_art(image_size=img_size,
                             bg_color=bg_clr,
                             num_lines=total_lines_in_img,
                             horizontal=horizontal,
                             vertical=vertical,
                             effect=effect_option)
    else:
        image = generate_art(image_size=img_size,
                             bg_color=bg_clr,
                             num_lines=total_lines_in_img,
                             horizontal=horizontal,
                             vertical=vertical,
                             start_color=start_clr,
                             end_color=end_clr,
                             effect=effect_option)

    images.append(image)
    next(cols).image(image, caption=f"{i + 1}")


