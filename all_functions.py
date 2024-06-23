import base64
import random
import colorsys
from io import BytesIO
from PIL import ImageChops, Image


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


def mirror_image(image):
    width, height = image.size
    mirrored_image = Image.new('RGB', (width, height))
    mirrored_image.paste(image.transpose(Image.FLIP_LEFT_RIGHT))

    return mirrored_image


def get_circle_cord(center, position, radius, style, max_size):
    circle_radius = random.randint(radius[0], radius[1])
    diameter = 2 * circle_radius

    x0 = 0
    x1 = 0
    y0 = 0
    y1 = 0

    if style == "Diagonal":
        # Check for overflow on all sides with a slight buffer for top
        overflow_left = center - position - radius[0] < 0
        overflow_right = center + position + radius[0] > max_size

        # Adjust position and/or radius to avoid overflow
        if overflow_left and overflow_right:
            # Circle cannot fit diagonally, adjust position to center
            position = 0
        elif overflow_left:
            # Overflow on the left, adjust position to fit
            position = max(position, center + radius[0])
        elif overflow_right:
            # Overflow on the right, adjust position to fit
            position = min(position, center - (max_size - radius[0]))

        # Recalculate y-coordinate based on adjusted position
        y0 = center - position
        y1 = y0 + diameter + position
        x0 = center - position
        x1 = x0 + diameter + position

    else:
        x0 = random.randint(-radius[0], max_size)  # Allow negative x0 for overflow
        y0 = random.randint(-radius[0], max_size)  # Allow negative y0 for overflow
        x1 = x0 + diameter
        y1 = y0 + diameter

    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0

    return (x0, y0), (x1, y1)


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
        # Randomly choose addition value within rect_size range
        addition = random.randint(rect_size[0], rect_size[1])

        # Calculate potential coordinates for diagonal placement
        center_adjusted_x = center_x - addition // 2
        y0 = position_y - addition // 2
        y1 = position_y + addition // 2
        x0 = center_adjusted_x
        x1 = center_adjusted_x + addition

        # Check for overflow on all sides with a slight buffer
        overflow_left = x0 < 0
        overflow_right = x1 > max_size
        overflow_top = y0 < 0
        overflow_bottom = y1 > max_size

        # Adjust position and/or size to avoid overflow while maintaining diagonality
        if overflow_left and overflow_top:
            # Special case: Top-left corner overflows
            # Adjust position and potentially shrink rectangle diagonally
            max_allowed_addition = min(center_x, max_size - position_y)
            adjusted_addition = min(addition, max_allowed_addition * 2)
            position_y = adjusted_addition // 2
            center_adjusted_x = max(0, center_x - adjusted_addition // 2)
            # Recalculate coordinates based on adjusted values
            y0 = position_y - adjusted_addition // 2
            y1 = position_y + adjusted_addition // 2
            x0 = center_adjusted_x
            x1 = center_adjusted_x + adjusted_addition
        else:
            # Handle other overflow cases
            if overflow_left:
                # Left side overflows, adjust position and potentially shrink rectangle
                position_y = min(position_y, addition // 2)
                center_adjusted_x = max(0, center_x - min(addition // 2, center_x))
                x0 = center_adjusted_x
                x1 = min(x1, max_size)  # Clip right side if needed
            elif overflow_right:
                # Right side overflows, adjust position and potentially shrink rectangle
                position_y = max(position_y, max_size - addition // 2)
                center_adjusted_x = min(max_size - addition // 2, center_x)
                x0 = max(x0, 0)  # Clip left side if needed
                x1 = center_adjusted_x + addition
            elif overflow_top:
                # Top side overflows, adjust position and potentially shrink rectangle
                position_y = max(position_y, addition // 2)
                y0 = max(y0, 0)
                y1 = min(y1, max_size)  # Clip bottom side if needed
            elif overflow_bottom:
                # Bottom side overflows, adjust position and potentially shrink rectangle
                position_y = min(position_y, max_size - addition // 2)
                y1 = min(y1, max_size)
                y0 = max(y0, 0)  # Clip top side if needed

        # Ensure y coordinates are in the correct order (y0 <= y1)
        if y0 > y1:
            y0, y1 = y1, y0

        return (x0-50, y0-50), (x1, y1)
    else:
        # For random style, generate random width and height within rect_size
        rect_width = random.randint(rect_size[0], rect_size[1])
        rect_height = random.randint(rect_size[0], rect_size[1])

        # Determine if rectangle extends outside the image bounds
        extend_outside = random.random() > 0.5

        if extend_outside:
            # Allow negative coordinates for extending outside the image
            x0 = random.randint(-rect_width, max_size)
            y0 = random.randint(-rect_height, max_size)
        else:
            # Ensure x and y coordinates are within image bounds
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
    width: 60%;
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
