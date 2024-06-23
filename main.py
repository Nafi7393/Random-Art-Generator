import random

from art_generator import generate_art
import image_functions
import streamlit as st
from itertools import cycle
import all_functions


st.set_page_config(page_title="Random Art Generator")
hide_menu = """
<style>#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>"""
st.markdown(hide_menu, unsafe_allow_html=True)

st.markdown("""
# _Random Art Generator_
######
###### made with [Python](https://www.python.org/) and [Pillow](https://pillow.readthedocs.io/en/stable/) Library.
""")

st.write("")
st.markdown(" ")
st.markdown(" ")


all_effects = ["NORMAL", "LIGHTER", "DIFFERENCE", "SCREEN", "ADD", "SUBTRACT",
               "ADD_MODULO", "SUBTRACT_MODULO", "random".upper()]

option = ["Horizontal", "Vertical", "Horizontal & Vertical", "Random Shape"]
circle_radius = (25, 200)
rectangle_size = 25
clr_choice = "Random"
design_style = "Random"
stoke = False
stroke_clr = None
stroke_width = 12
seamless_bool = False
padding = False


image_type = st.sidebar.selectbox(label="What shapes you want?".upper(), options=["Line", "Circle", "Rectangle"])
total_img = st.sidebar.slider(label="Total How Many Images", min_value=1, max_value=25, value=2)
img_size = st.sidebar.slider(label="Image Size", min_value=128, max_value=3450, value=720)


with st.sidebar.form(key="Image Details"):
    if image_type == "Line":
        img_option = st.selectbox(label="What type of image you want?".upper(), options=option)
        type_str = "Total Number of Lines"
        min_val = 5
        max_val = 50
        value = 10

    elif image_type == "Circle":
        img_option = "Circle"
        type_str = "Total Number of Circles"
        min_val = 5
        max_val = 200
        value = 50

    elif image_type == "Rectangle":
        img_option = "Rectangle"
        type_str = "Total Number of Rectangles"
        min_val = 5
        max_val = 200
        value = 50

    if image_type in ["Circle", "Rectangle"]:
        design_style = st.selectbox(label="What Design Style you want?".upper(), options=["Diagonal", "Random"])
        seamless_bool = False

    st.write(" ")
    st.write(" ")

    total_lines_in_img = st.slider(label=type_str, min_value=min_val, max_value=max_val, value=value)
    if img_option == "Random Shape":
        padding = st.slider(label="Padding Value", min_value=-(img_size // 5), max_value=img_size // 5, value=0)
    else:
        padding = False

    if image_type == "Circle":
        # Increase base values proportionally to image size
        min_v_cir = int(img_size * 0.05) + 20  # Adjust for larger base minimum radius
        max_v_cir = int(img_size * 0.7) + 200  # Adjust for larger base maximum radius

        # Calculate fractions for initial values based on range
        fraction_min = 1 / 10  # Adjust for more spread towards minimum radius
        fraction_max = 1 / 2  # Adjust for wider range towards maximum radius

        initial_min_radius = min_v_cir + int((max_v_cir - min_v_cir) * fraction_min)
        initial_max_radius = max_v_cir - int((max_v_cir - min_v_cir) * fraction_max)

        circle_radius = st.slider(label="Minimum and Maximum Radius", min_value=min_v_cir, max_value=max_v_cir,
                                  value=(initial_min_radius, initial_max_radius))

    if image_type == "Rectangle":
        # Increase base values proportionally to image size
        min_v_rec = int(img_size * 0.2) + 50  # Adjust for larger base minimum rectangle size
        max_v_rec = int(img_size * 0.8) + 300  # Adjust for larger base maximum rectangle size

        # Calculate fractions for initial values based on range
        fraction_min = 1 / 3  # Adjust for spread towards minimum size
        fraction_max = 1 / 6  # Adjust for wider range towards maximum size

        initial_min_size = min_v_rec + int((max_v_rec - min_v_rec) * fraction_min)
        initial_max_size = max_v_rec - int((max_v_rec - min_v_rec) * fraction_max)

        rectangle_size = st.slider(label="Minimum and Maximum Size of Rectangle",
                                   min_value=min_v_rec, max_value=max_v_rec,
                                   value=(initial_min_size, initial_max_size))

    st.markdown("---")
    st.markdown(" ")

    dots = st.checkbox(label="Add Small DOTs")
    num_of_dots = st.slider(label="Number of Total Small Dots", min_value=10, max_value=600, value=150)
    dot_clr = all_functions.hex_to_rgb(st.color_picker(label="Set Dot Color", value="#ffffff"))

    st.markdown("---")

    background_clr_choice = st.radio(label="Set Background Color", options=("Random", "Pick One"))
    st.write("<style>div.row-widget.stRadio > div{flex-direction:row;}</style>", unsafe_allow_html=True)
    background_clr = st.color_picker(label="Only if you choose 'Pick One' from above")
    st.markdown("---")
    clr_choice = st.radio(label="Set Fill Color", options=("Random", "Pick One"))
    st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
    st.write('<p style="font-size: 14px;">Only if you choose "Pick One" from above</p>', unsafe_allow_html=True)

    clr1, clr2 = st.columns(2)
    with clr1:
        start_clr = all_functions.hex_to_rgb(st.color_picker(label="Start Color"))
    with clr2:
        end_clr = all_functions.hex_to_rgb(st.color_picker(label="End Color"))
    st.markdown("---")

    if image_type == "Circle":
        stoke = st.checkbox("Give Circle a Stroke")
        stroke_clr_option = st.radio( label="Set Stroke Color (Only if you Check the above Box)",
                                      options=("Random", "Pick One"))
        st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
        st.write('<p style="font-size: 14px;">Only if you choose "Pick One" from above</p>', unsafe_allow_html=True)
        stroke_clr = all_functions.hex_to_rgb(st.color_picker(label="Stroke Color"))
        stroke_width = st.slider(label="Set The Stroke Width", min_value=1, max_value=100, value=12)
        st.markdown("---")

    if image_type == "Rectangle":
        stoke = st.checkbox("Give Rectangle a Stroke")
        stroke_clr_option = st.radio(label="Set Stroke Color (Only if you Check the above Box)",
                                     options=("Random", "Pick One"))
        st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
        st.write('<p style="font-size: 14px;">Only if you choose "Pick One" from above</p>',unsafe_allow_html=True)
        stroke_clr = all_functions.hex_to_rgb(st.color_picker(label="Stroke Color"))
        stroke_width = st.slider(label="Set The Stroke Width", min_value=1, max_value=100, value=12)
        st.markdown("---")

    st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
    st.write('<p style="font-size: 15px;">If you want a seamless pattern!</p>'.upper(), unsafe_allow_html=True)
    pattern = st.checkbox("Seamless Pattern", value=seamless_bool)
    st.markdown("---")

    effect_option = st.selectbox(label="What type of image you want?", options=all_effects, index=8)

    submit = st.form_submit_button(label="SUBMIT")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("""
        <style>
        .submit-button {
            background: linear-gradient(135deg, #6d5dfc, #c3c3fc);
            border: none;
            border-radius: 25px;
            color: white;
            padding: 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
            cursor: pointer;
            box-shadow: 0 8px 10px rgba(0, 0, 0, 0.4);
            transition: all 0.4s ease;
            width: 100%;
        }
        
        .submit-button:hover {
            background: linear-gradient(135deg, #42a5f5, #478ed1);
            box-shadow: 0 5px 5px rgba(0, 0, 0, 0.5);
            transform: translateY(-3px);
            border-color: #42a5f5 !important;
            color: white !important;
        }
        
        .submit-button:active {
            opacity: 0.4;
            background: linear-gradient(135deg, #5d59f9, #b2b2fc) !important;
            color: white !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2) !important;
            transform: translateY(10px) !important;
            border-color: #6d5dfc !important;
        }
        
        .submit-button:focus {
            background: linear-gradient(135deg, #6d5dfc, #c3c3fc) !important;
            color: #ffffff !important;
            border-color: none !important;
            outline: none !important;
              &:focus {
                outline: none;
              }
        }
        </style>
        """, unsafe_allow_html=True)


circle = False
horizontal = False
vertical = False
rectangle = False
random_line = False


if image_type == "Line":
    if img_option == option[0]:
        horizontal = True
    elif img_option == option[1]:
        vertical = True
    elif img_option == option[2]:
        horizontal = True
        vertical = True
    elif img_option == option[3]:
        random_line = True

elif image_type == "Circle":
    circle = True
elif image_type == "Rectangle":
    rectangle = True


images = []
size = 7
cols = cycle(st.columns([size, 1, size]))

effect_random = False
if effect_option == "RANDOM":
    effect_random = True
for i in range(total_img):
    if background_clr_choice == "Random":
        bg_clr = all_functions.rand_clr()
    else:
        bg_clr = background_clr

    if stoke:
        if stroke_clr_option == "Random":
            stroke_clr = all_functions.rand_clr()

    if effect_random:
        effect_option = random.choice(all_effects[:-1])

    if clr_choice != "Pick One":
        image = generate_art(image_size=img_size, bg_color=bg_clr, num_lines=total_lines_in_img, horizontal=horizontal,
                             vertical=vertical, random_line=random_line, circle=circle, rect=rectangle,
                             stroke_clr=stroke_clr, cir_radius=circle_radius, rectangle_size=rectangle_size,
                             stroke_width=stroke_width, style=design_style, small_dots=dots, num_of_dots=num_of_dots,
                             dot_clr=dot_clr, effect=effect_option, padding_=padding)
    else:
        image = generate_art(image_size=img_size, bg_color=bg_clr, num_lines=total_lines_in_img, horizontal=horizontal,
                             vertical=vertical, circle=circle, rect=rectangle, random_line=random_line, padding_=padding,
                             start_color=start_clr, end_color=end_clr, stroke_clr=stroke_clr, cir_radius=circle_radius,
                             rectangle_size=rectangle_size, stroke_width=stroke_width, style=design_style,
                             small_dots=dots, num_of_dots=num_of_dots, dot_clr=dot_clr, effect=effect_option)
    if pattern:
        image = image_functions.make_seamless(img=image, image_size=img_size)

    images.append(image)
    download_link = all_functions.image_download(image, f"Image_{i+1}")

    this_col = next(cols)
    if i % 2 != 0:
        this_col = next(cols)
    this_col.image(image, caption=f"{img_option} {i + 1} --- Effect: {effect_option}")
    this_col.write(download_link, unsafe_allow_html=True)
    this_col.write(" ")
    this_col.write(" ")
    this_col.write(" ")
    this_col.write(" ")
