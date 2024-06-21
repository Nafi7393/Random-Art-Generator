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


def get_circle_cord(center, position, radius, style, max_size):
    """
    Generate circle coordinates based on center, position,
    radius, style, and max_size. Circles may overflow the image bounds.

    Parameters:
    - center (int): Center coordinate of the circle.
    - position (int): Position offset of the circle.
    - radius (tuple): Tuple (min_radius, max_radius) specifying the minimum
                      and maximum radius of the circle.
    - style (str): Style of the circle ('Random' or any other value).
    - max_size (int): Maximum size of the image (image_size_px).

    Returns:
    - tuple: Tuple containing coordinates (left_point, right_point) of the circle.
    """

    # Calculate addition within reasonable limits to ensure circles stay within bounds
    addition = random.randint(radius[0], radius[1] + 50)

    # Calculate top and bottom coordinates allowing overflow if necessary
    top = random.randint(-addition, max_size)
    bottom = top + addition
    if bottom > max_size:
        bottom = max_size

    # Calculate left and right coordinates allowing overflow if necessary
    left = random.randint(-addition, max_size)
    right = left + addition
    if right > max_size:
        right = max_size

    return (left, top), (right, bottom)



def get_rect_cord(center_x, position_y, rect_size, style, max_size):
    """
    Generate rectangle coordinates based on center_x, position_y,
    rect_size, style, and max_size.

    Parameters:
    - center_x (int): X-coordinate of the center of the rectangle.
    - position_y (int): Y-coordinate of the position of the rectangle.
    - rect_size (tuple): Tuple (min_size, max_size) specifying the minimum
                         and maximum size of the rectangle.
    - style (str): Style of the rectangle ('Random' or 'Diagonal').
    - max_size (int): Maximum size of the image (image_size_px).

    Returns:
    - tuple: Tuple containing coordinates (left_point, right_point) of the rectangle.
    """

    if style == "Diagonal":
        # For diagonal style, place rectangles along a diagonal line
        addition = random.randint(rect_size[0], rect_size[1])

        # Ensure y coordinates stay within image bounds
        y0 = max(0, min(position_y, max_size - addition))
        y1 = max(0, min(position_y + addition, max_size))
        if y0 > y1:
            y0, y1 = y1, y0

        # Ensure x coordinates stay within image bounds
        x0 = max(0, min(center_x - addition // 2, max_size - addition))
        x1 = max(0, min(center_x + addition // 2, max_size))
        if x0 > x1:
            x0, x1 = x1, x0

        return (x0, y0), (x1, y1)
    else:
        # For random style, place rectangles randomly within and outside the image bounds
        rect_width = random.randint(rect_size[0], rect_size[1])
        rect_height = random.randint(rect_size[0], rect_size[1])

        # Randomly decide whether to extend outside the image
        extend_outside = random.random() > 0.5

        if extend_outside:
            x0 = random.randint(-rect_width, max_size)
            y0 = random.randint(-rect_height, max_size)
        else:
            x0 = random.randint(0, max_size - rect_width)
            y0 = random.randint(0, max_size - rect_height)

        x1 = x0 + rect_width
        y1 = y0 + rect_height

        return (x0, y0), (x1, y1)


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
