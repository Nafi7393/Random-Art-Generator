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


def random_lines_draw(image, image_size_px, padding, num_lines, thickness_scale, start_color, end_color, effect):
    points = []

    # Generate random points within the padded area
    for _ in range(num_lines):
        point = (all_functions.random_point(image_size_px - 2 * padding, padding) + padding,
                 all_functions.random_point(image_size_px - 2 * padding, padding) + padding)
        points.append(point)

    # Calculate the bounding box of all points
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    # Calculate offsets to center the points in the image
    x_offset = (image_size_px - max_x - min_x) // 2
    y_offset = (image_size_px - max_y - min_y) // 2

    # Apply offsets to center the points
    for i, point in enumerate(points):
        points[i] = (point[0] + x_offset, point[1] + y_offset)

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
            overlay_draw.line([point, next_point], fill=line_color, width=current_thickness)

            image = all_functions.image_effect(image, overlay_image, effect)

        current_thickness += thickness_scale

    return image


def circle_image(image, image_size_px, num_circle, radius, start_color, end_color,
                 stroke_color, effect, style, stroke_width=15):
    n_points = num_circle - 1
    drawing = ImageDraw.Draw(image)

    for i in range(num_circle):
        circle_center = random.randint(0, image_size_px)
        position = random.randint(0, image_size_px)
        left_point, right_point = all_functions.get_circle_cord(circle_center, position, radius, style, image_size_px)

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


def rect_image(image, image_size_px, num_rect, start_color, end_color, stroke_color,
               rect_size, style, effect, stroke_width=15):

    n_points = num_rect - 1
    drawing = ImageDraw.Draw(image)

    # Calculate spacing between rectangles to evenly distribute them
    step_x = image_size_px // (num_rect + 1)
    step_y = image_size_px // (num_rect + 1)

    for i in range(num_rect):
        # Calculate center of each rectangle
        circle_center = step_x * (i + 1)
        position = step_y * (i + 1)

        # Generate rectangle coordinates
        left_point, right_point = all_functions.get_rect_cord(
            circle_center, position, rect_size, style, image_size_px
        )

        # Interpolate color based on position in sequence
        factor = i / n_points
        line_color = all_functions.interpolate(start_color, end_color, factor=factor)

        # Draw the rectangle
        points = (left_point, right_point)
        if effect == "normal":
            drawing.rectangle(points, fill=line_color, outline=stroke_color, width=stroke_width)
        else:
            overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay_image)
            overlay_draw.rectangle(points, fill=line_color, outline=stroke_color, width=stroke_width)
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
