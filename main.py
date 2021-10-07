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


all_effects = ["lighter".upper(), "difference".upper(), "screen".upper(), "add".upper(), "subtract".upper()]
option = ["Horizontal", "Vertical", "Horizontal & Vertical", "Random Shape"]
circle_radius = (25, 200)
rectangle_size = 25
clr_choice = "Random"
design_style = "Random"
stoke = False
stroke_clr = None
stroke_width = 12
seamless_bool = False


image_type = st.sidebar.selectbox(label="What shapes you want?".upper(), options=["Line", "Circle", "Rectangle"])
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
        max_val = 100
        value = 20

    elif image_type == "Rectangle":
        img_option = "Rectangle"
        type_str = "Total Number of Rectangles"
        min_val = 5
        max_val = 80
        value = 15

    if image_type in ["Circle", "Rectangle"]:
        design_style = st.selectbox(label="What Design Style you want?".upper(), options=["Diagonal", "Random"])
        seamless_bool = True

    total_lines_in_img = st.slider(label=type_str, min_value=min_val, max_value=max_val, value=value)
    if image_type == "Circle":
        min_v = (img_size//27) + 5
        max_v = (img_size//3) + 50
        circle_radius = st.slider(label="Minimum and Maximum Radius",
                                  min_value=min_v, max_value=max_v,
                                  value=(min_v, round((((max_v - 70)-min_v)/(max_v - 70)) * 100) - 70))

    if image_type == "Rectangle":
        min_v_rec = (img_size//7) + 10
        max_v_rec = (img_size//2) + 80
        rectangle_size = st.slider(label="Minimum and Maximum Size of Rectangle",
                                   min_value=min_v_rec, max_value=max_v_rec,
                                   value=(min_v_rec, round((((max_v_rec - 80)-min_v_rec)/(max_v_rec - 80)) * 100) - 50))

    total_img = st.slider(label="Total How Many Images", min_value=1, max_value=25, value=1)
    st.markdown("---")

    background_clr_choice = st.radio(label="Set Background Color", options=('Random', 'Pick One'))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    background_clr = st.color_picker(label="Only if you choose 'Pick One' from above")
    st.markdown("---")

    clr_choice = st.radio(label="Set Fill Color", options=('Random', 'Pick One'))
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
        stroke_clr_option = st.radio(label="Set Stroke Color (Only if you Check the above Box)",
                                     options=('Random', 'Pick One'))
        st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
        st.write('<p style="font-size: 14px;">Only if you choose "Pick One" from above</p>', unsafe_allow_html=True)
        stroke_clr = all_functions.hex_to_rgb(st.color_picker(label="Stroke Color"))
        stroke_width = st.slider(label="Set The Stroke Width", min_value=1, max_value=100, value=12)
        st.markdown("---")

    if image_type == "Rectangle":
        stoke = st.checkbox("Give Rectangle a Stroke")
        stroke_clr_option = st.radio(label="Set Stroke Color (Only if you Check the above Box)",
                                     options=('Random', 'Pick One'))
        st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
        st.write('<p style="font-size: 14px;">Only if you choose "Pick One" from above</p>', unsafe_allow_html=True)
        stroke_clr = all_functions.hex_to_rgb(st.color_picker(label="Stroke Color"))
        stroke_width = st.slider(label="Set The Stroke Width", min_value=1, max_value=100, value=12)
        st.markdown("---")

    st.write('<p style="font-size: 13.5px;"> </p>', unsafe_allow_html=True)
    st.write('<p style="font-size: 15px;">If you want a seamless pattern!</p>'.upper(), unsafe_allow_html=True)
    pattern = st.checkbox("Seamless Pattern", value=seamless_bool)
    st.markdown("---")

    effect_option = st.selectbox(label="What type of image you want?", options=all_effects, index=3)

    submit = st.form_submit_button()


images = []
cols = cycle(st.columns(2))


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


for i in range(total_img):
    if background_clr_choice == "Random":
        bg_clr = all_functions.rand_clr()
    else:
        bg_clr = background_clr

    if stoke:
        if stroke_clr_option == "Random":
            stroke_clr = all_functions.rand_clr()

    if clr_choice != "Pick One":
        image = generate_art(image_size=img_size,
                             bg_color=bg_clr,
                             num_lines=total_lines_in_img,
                             horizontal=horizontal,
                             vertical=vertical,
                             random_line=random_line,
                             circle=circle,
                             rect=rectangle,
                             stroke_clr=stroke_clr,
                             cir_radius=circle_radius,
                             rectangle_size=rectangle_size,
                             stroke_width=stroke_width,
                             style=design_style,
                             effect=effect_option)
    else:
        image = generate_art(image_size=img_size,
                             bg_color=bg_clr,
                             num_lines=total_lines_in_img,
                             horizontal=horizontal,
                             vertical=vertical,
                             circle=circle,
                             rect=rectangle,
                             random_line=random_line,
                             start_color=start_clr,
                             end_color=end_clr,
                             stroke_clr=stroke_clr,
                             cir_radius=circle_radius,
                             rectangle_size=rectangle_size,
                             stroke_width=stroke_width,
                             style=design_style,
                             effect=effect_option)
    if pattern:
        image = image_functions.make_seamless(img=image, image_size=img_size)

    images.append(image)
    download_link = all_functions.image_download(image, f'Image_{i+1}')

    this_col = next(cols)
    this_col.image(image, caption=f'{img_option} {i + 1}')
    this_col.write(download_link, unsafe_allow_html=True)




