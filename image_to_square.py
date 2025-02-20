import math

from PIL import Image


def next_power_of_2_exponent(n):
    return math.ceil(math.log2(n))


def make_square(image_path, output_path, fill_color=(255, 255, 255)):
    image = Image.open(image_path)
    width, height = image.size
    max_side = max(width, height)
    side = 2 ** next_power_of_2_exponent(max_side)

    new_image = Image.new("RGB", (side, side), fill_color)

    paste_position = ((side - width) // 2, (side - height) // 2)
    new_image.paste(image, paste_position)

    new_image.save(output_path)


make_square("imag.jpg", "ro2.jpeg")
