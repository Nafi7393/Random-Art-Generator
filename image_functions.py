import all_functions
from PIL import Image, ImageDraw, ImageOps
import random


def horizontal_line_draw(
    image, image_size_px, num_lines, thickness_scale, start_color, end_color, effect
):
    current_thickness = thickness_scale
    n_points = num_lines - 1
    max_distance = image_size_px // 13

    drawing = ImageDraw.Draw(image)

    for i in range(num_lines):
        top_point = (random.randint(0, image_size_px), 0)
        bottom_point = (
            random.randint(top_point[0] - max_distance, top_point[0] + max_distance),
            image_size_px,
        )

        factor = i / n_points
        line_color = all_functions.interpolate(start_color, end_color, factor=factor)

        if effect == "normal":
            drawing.line(
                [top_point, bottom_point], fill=line_color, width=current_thickness
            )
        else:
            overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay_image)
            overlay_draw.line(
                [top_point, bottom_point], fill=line_color, width=current_thickness
            )
            image = all_functions.image_effect(image, overlay_image, effect)

        current_thickness += thickness_scale

    return image


def vertical_line_draw(
    image, image_size_px, num_lines, thickness_scale, start_color, end_color, effect
):
    current_thickness = thickness_scale
    n_points = num_lines - 1
    max_distance = image_size_px // 13

    drawing = ImageDraw.Draw(image)

    for i in range(num_lines):
        left_point = (0, random.randint(0, image_size_px))
        right_point = (
            image_size_px,
            random.randint(left_point[1] - max_distance, left_point[1] + max_distance),
        )

        factor = i / n_points
        line_color = all_functions.interpolate(start_color, end_color, factor=factor)

        if effect == "normal":
            drawing.line(
                [left_point, right_point], fill=line_color, width=current_thickness
            )
        else:
            overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay_image)
            overlay_draw.line(
                [left_point, right_point], fill=line_color, width=current_thickness
            )
            image = all_functions.image_effect(image, overlay_image, effect)

        current_thickness += thickness_scale

    return image


def random_lines_draw(
    image,
    image_size_px,
    padding,
    num_lines,
    thickness_scale,
    start_color,
    end_color,
    effect,
):

    points = []

    for _ in range(num_lines):
        point = (
            all_functions.random_point(image_size_px, padding),
            all_functions.random_point(image_size_px, padding),
        )
        points.append(point)

    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    x_offset = (min_x - padding) - (image_size_px - padding - max_x)
    y_offset = (min_y - padding) - (image_size_px - padding - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - x_offset // 2, point[1] - y_offset // 2)

    current_thickness = thickness_scale
    n_points = len(points) - 1

    drawing = ImageDraw.Draw(image)

    for i, point in enumerate(points):
        if i == n_points:
            next_point = points[0]
        else:
            next_point = points[i + 1]

        factor = i / n_points
        line_color = all_functions.interpolate(start_color, end_color, factor=factor)

        if effect == "normal":
            drawing.line([point, next_point], fill=line_color, width=current_thickness)
        else:
            overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay_image)
            overlay_draw.line(
                [point, next_point], fill=line_color, width=current_thickness
            )

            image = all_functions.image_effect(image, overlay_image, effect)
        current_thickness += thickness_scale

    return image


def circle_image(
    image,
    image_size_px,
    num_circle,
    radius,
    start_color,
    end_color,
    stroke_color,
    effect,
    style,
    stroke_width=15,
):

    n_points = num_circle - 1
    drawing = ImageDraw.Draw(image)

    for i in range(num_circle):
        circle_center = random.randint(0, image_size_px)
        position = random.randint(0, image_size_px)
        left_point, right_point = all_functions.get_circle_cord(
            circle_center, position, radius, style
        )

        factor = i / n_points
        line_color = all_functions.interpolate(start_color, end_color, factor=factor)

        if effect == "normal":
            drawing.ellipse(
                [left_point, right_point],
                fill=line_color,
                outline=stroke_color,
                width=stroke_width,
            )
        else:
            overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay_image)
            overlay_draw.ellipse(
                [left_point, right_point],
                fill=line_color,
                outline=stroke_color,
                width=stroke_width,
            )
            image = all_functions.image_effect(image, overlay_image, effect)

    return image


def rect_image(
    image,
    image_size_px,
    num_rect,
    start_color,
    end_color,
    stroke_color,
    rect_size,
    style,
    effect,
    stroke_width=15,
):

    n_points = num_rect - 1
    drawing = ImageDraw.Draw(image)

    for i in range(num_rect):
        circle_center = random.randint(0, image_size_px)
        position = random.randint(0, image_size_px)
        left_point, right_point = all_functions.get_rect_cord(
            circle_center, position, rect_size, style
        )

        factor = i / n_points
        line_color = all_functions.interpolate(start_color, end_color, factor=factor)

        if effect == "normal":
            drawing.rectangle(
                [left_point, right_point],
                fill=line_color,
                outline=stroke_color,
                width=stroke_width,
            )
        else:
            overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay_image)
            overlay_draw.rectangle(
                [left_point, right_point],
                fill=line_color,
                outline=stroke_color,
                width=stroke_width,
            )
            image = all_functions.image_effect(image, overlay_image, effect)

    return image


def make_small_dots(image, image_size_px, color, number_of_dots=100):
    drawing = ImageDraw.Draw(image)
    min_size = image_size_px // 150
    max_size = image_size_px // 70

    for i in range(number_of_dots):
        x1 = random.randint(0, image_size_px)
        y1 = random.randint(0, image_size_px)
        size_expand = random.randint(min_size, max_size)

        drawing.ellipse([(x1, y1), (x1 + size_expand, y1 + size_expand)], fill=color)

    return image


def make_seamless(img, image_size):
    pat_size = image_size * 2
    image = Image.new("RGB", (pat_size, pat_size), (0, 0, 0))
    image.paste(img, (0, 0))

    transposed = ImageOps.mirror(img)
    image.paste(transposed, (image_size, 0))

    image.paste(ImageOps.flip(img), (0, image_size))
    image.paste(ImageOps.flip(transposed), (image_size, image_size))

    return image
