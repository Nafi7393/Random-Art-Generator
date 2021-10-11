import base64
import random
import colorsys
from io import BytesIO
from PIL import ImageChops


def rand_clr():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def random_point(image_size_px: int, padding: int):
    return random.randint(padding, image_size_px - padding)


def random_color():

    # I want a bright, vivid color, so max V and S and only randomize HUE.
    h = random.random()
    s = 1
    v = 1
    float_rbg = colorsys.hsv_to_rgb(h, s, v)

    # Return as integer RGB.
    return (
        int(float_rbg[0] * 255),
        int(float_rbg[1] * 255),
        int(float_rbg[2] * 255),
    )


def interpolate(start_color, end_color, factor: float):
    # Find the color that is exactly factor (0.0 - 1.0) between the two colors.
    new_color_rgb = []
    for i in range(3):
        new_color_value = factor * end_color[i] + (1 - factor) * start_color[i]
        new_color_rgb.append(int(new_color_value))

    return tuple(new_color_rgb)


def image_effect(back_image, front_line, effect):
    all_effects = [
        "lighter",
        "darker",
        "difference",
        "multiply",
        "screen",
        "soft_light",
        "hard_light",
        "overlay",
        "add",
        "subtract",
        "add_modulo",
        "subtract_modulo",
        "logical_and",
        "logical_or",
        "logical_xor",
    ]

    the_effect = f"ImageChops.{effect}(back_image, front_line)"
    return eval(the_effect)


def get_circle_cord(center, position, radius, style):
    addition = random.randint(radius[0], radius[1] + 50)
    top = random.randint(0, center + position)
    bottom = random.randint(0, center + position)
    left = top + addition
    right = bottom + addition

    if style == "Random":
        return (top, bottom), (left, right)
    else:
        return (top, top), (bottom, bottom)


def get_rect_cord(center, position, size, style):
    addition = random.randint(size[0], size[1] + 50)
    top = random.randint(0, center + position)
    bottom = random.randint(0, center + position)
    left = top + random.randint(size[0], addition)
    right = bottom + random.randint(size[0], addition)

    if style == "Random":
        return (top, bottom), (left, right)
    else:
        return (top, top), (bottom, bottom)


def image_download(img, file_name):
    style = """
    border: none;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
    text-decoration: none;
    background-color: #0D58B1;
    color: #FFFB00;
    text-align: center;
    padding: 10px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    display: inline-block;
    border-radius: 15px;
    """

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/jpg;base64,{img_str}" class="btn download" style="{style}" download={file_name}.jpg>DOWNLOAD IMAGE {file_name[6:]}</a>'
    return href
