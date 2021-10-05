from PIL import Image
import all_functions
import image_functions


def generate_art(image_size, bg_color=(0, 0, 0), num_lines=10,
                 horizontal=False, vertical=False, circle=False, rect=False,
                 cir_radius=(), stroke_clr=None, stroke_width=12,
                 rectangle_size=(), style=None,
                 start_color=None, end_color=None, padding_=True, effect="add"):

    # Set size parameters.
    rescale = 2
    image_size_px = image_size * rescale
    pad = image_size // 15
    effect = effect.lower()

    if num_lines <= 10:
        thickness_scale = round(image_size / 170)
    elif 10 < num_lines <= 20:
        thickness_scale = round(image_size / 220)
    elif 20 < num_lines <= 30:
        thickness_scale = round(image_size / 290)
    elif 30 < num_lines <= 40:
        thickness_scale = round(image_size / 390)
    elif 40 < num_lines <= 50:
        thickness_scale = round(image_size / 500)
    else:
        thickness_scale = round(image_size / 650)

    if horizontal or vertical or circle or rect:
        padding_ = False

    if padding_:
        padding = pad * rescale
    else:
        padding = 0

    # Create the directory and base image.
    image = Image.new("RGB", (image_size_px, image_size_px), bg_color)

    # Pick the colors.
    if not start_color:
        start_color = all_functions.random_color()
    if not end_color:
        end_color = all_functions.random_color()

    # get the image
    if horizontal:
        image = image_functions.horizontal_line_draw(image, image_size_px, num_lines, thickness_scale, start_color, end_color, effect)
    elif vertical:
        image = image_functions.vertical_line_draw(image, image_size_px, num_lines, thickness_scale, start_color, end_color, effect)
    elif circle:
        image = image_functions.circle_image(image, image_size_px, num_circle=num_lines, radius=cir_radius,
                                             stroke_width=stroke_width,
                                             start_color=start_color, end_color=end_color, stroke_color=stroke_clr,
                                             effect=effect, style=style)
    elif rect:
        image = image_functions.rect_image(image, image_size_px, num_rect=num_lines,
                                           start_color=start_color, end_color=end_color, stroke_color=stroke_clr,
                                           rect_size=rectangle_size, style=style,
                                           effect=effect, stroke_width=15)
    else:
        image = image_functions.random_lines_draw(image, image_size_px, padding, num_lines, thickness_scale, start_color, end_color, effect)

    # Image is done! Now resize it to be smooth.
    image = image.resize(
        (image_size_px // rescale, image_size_px // rescale), resample=Image.ANTIALIAS
    )

    # Return the image.
    return image


