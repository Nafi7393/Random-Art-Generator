from PIL import Image
import all_functions
import image_functions


def generate_art(
    image_size,
    bg_color=(0, 0, 0),
    num_lines=10,
    horizontal=False,
    vertical=False,
    circle=False,
    rect=False,
    random_line=False,
    cir_radius=(),
    stroke_clr=None,
    stroke_width=12,
    rectangle_size=(),
    style=None,
    small_dots=False,
    num_of_dots=100,
    dot_clr=(255, 255, 255),
    start_color=None,
    end_color=None,
    padding_=False,
    effect="add",
):

    # Set size parameters.
    rescale = 2
    image_size_px = image_size * rescale
    pad = image_size // 20
    effect = effect.lower()
    thick_addition = -20

    if num_lines <= 10:
        thickness_scale = round(image_size / (150 + thick_addition))
    elif 10 < num_lines <= 20:
        thickness_scale = round(image_size / (200 + thick_addition))
    elif 20 < num_lines <= 30:
        thickness_scale = round(image_size / (300 + thick_addition))
    elif 30 < num_lines <= 40:
        thickness_scale = round(image_size / (420 + thick_addition))
    elif 40 < num_lines <= 50:
        thickness_scale = round(image_size / (600 + thick_addition))
    else:
        thickness_scale = round(image_size / (750 + thick_addition))

    if not padding_:
        padding = 0
    else:
        padding = padding_

    # Create the directory and base image.
    image = Image.new("RGB", (image_size_px, image_size_px), bg_color)

    # Pick the colors.
    if not start_color:
        start_color = all_functions.random_color()
    if not end_color:
        end_color = all_functions.random_color()

    # get the image
    if small_dots:
        image = image_functions.make_small_dots(
            image=image,
            image_size_px=image_size_px,
            color=dot_clr,
            number_of_dots=num_of_dots,
        )

    if horizontal:
        image = image_functions.horizontal_line_draw(
            image=image,
            image_size_px=image_size_px,
            num_lines=num_lines,
            thickness_scale=thickness_scale,
            start_color=start_color,
            end_color=end_color,
            effect=effect,
        )
    if vertical:
        image = image_functions.vertical_line_draw(
            image=image,
            image_size_px=image_size_px,
            num_lines=num_lines,
            thickness_scale=thickness_scale,
            start_color=start_color,
            end_color=end_color,
            effect=effect,
        )
    if random_line:
        image = image_functions.random_lines_draw(
            image=image,
            image_size_px=image_size_px,
            padding=padding,
            num_lines=num_lines,
            thickness_scale=thickness_scale,
            start_color=start_color,
            end_color=end_color,
            effect=effect,
        )
    if circle:
        image = image_functions.circle_image(
            image=image,
            image_size_px=image_size_px,
            num_circle=num_lines,
            radius=cir_radius,
            stroke_width=stroke_width,
            start_color=start_color,
            end_color=end_color,
            stroke_color=stroke_clr,
            effect=effect,
            style=style,
        )
    if rect:
        image = image_functions.rect_image(
            image=image,
            image_size_px=image_size_px,
            num_rect=num_lines,
            start_color=start_color,
            end_color=end_color,
            stroke_color=stroke_clr,
            rect_size=rectangle_size,
            style=style,
            effect=effect,
            stroke_width=15,
        )

    # Image is done! Now resize it to be smooth.
    image = image.resize(
        (image_size_px // rescale, image_size_px // rescale), resample=Image.ANTIALIAS
    )

    # Return the image.
    return image
