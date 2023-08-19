from PIL import Image, ImageDraw
from PIL import ImageFont
from os_tools import tools as tools

"""
  NOTICE: These whole library heavily relied upon PIL.
  To make sure everything works correctly, install PIL like this:
  
    pip3.11 uninstall pillow           # remove existing package
    brew install libimagequant     # added support for png compression
    brew install zlib              # added support for png compression
    brew install libraqm  # for supporting hebrew and other rtl languages
    export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"  # export all these to the path
    pip3.11 install --upgrade Pillow --global-option="build_ext" --global-option="--enable-imagequant" --global-option="--enable-zlib" --global-option="--vendor-raqm"

  *Taken from here:
  https://stackoverflow.com/a/61969447/4036390
"""


def load_img(img_path):
    """Will load image to a variable.

    Parameters:
    :param img_path: the path to the image file
    :return image file to work on
    """
    img = Image.open(img_path)
    return img.convert('RGBA')


def create_new_image(width,
                     height,
                     fixed_background_color=None,
                     gradient_background_color_start=None,
                     gradient_background_color_end=None):
    """Will create a new image

    Parameters:
    :param width: the width of the new image
    :param height: the height of the new image
    :param fixed_background_color: (optional) a static background color (none for transparent)
    :param gradient_background_color_start: (optional) for a gradient background color, this will be the starting color
    :param gradient_background_color_end: (optional) for a gradient background color, this will be the ending color
    """
    if fixed_background_color is None:
        fixed_background_color = (255, 0, 0, 0)
        image = Image.new('RGBA', (width, height), fixed_background_color)
    else:
        image = Image.new('RGBA', (width, height), tools.hex_to_rgb(fixed_background_color))

    if gradient_background_color_start is not None and gradient_background_color_end is not None:
        image = set_gradient(width, height, gradient_background_color_start, gradient_background_color_end)
    return image


def tilt_image(image, degrees, resize_factor_for_antialiasing=1):
    """Will tilt an image by degrees.
    In reality, any tilt of an image file will cause a distortion of the pixels. It essentially means that
    when you'll paste the image on your canvas the image will look 'choppy'. To fix this, if you're using a lossless image format
    like a .png, you can set a resize_factor_for_antialiasing to raise the width and height of the image pre tilt and revent to the
    original props when the tilt completes. This will eliminate the choppy pixels

    Parameters:
    :param image: the image you loaded (from load_img)
    :param degrees: the degrees to tilt
    :param resize_factor_for_antialiasing: change this to other number. Will probably prevent the choppy pixels in a loseless image format
    :return the tilted image
    """
    original_image_height = image.height
    original_image_width = image.width
    new_image = resize_img_by_height(image, original_image_height * resize_factor_for_antialiasing)
    new_image = new_image.rotate(degrees, expand=1)
    new_image = resize_img_by_width_and_height(new_image, original_image_width, original_image_height)
    return new_image


def paste_image(background_img, img_to_paste, x, y):
    """Will paste image on a given background

    Parameters:
    :param background_img: the img which will be served as the background
    (load it from load_img)
    :param img_to_paste: the image to paste on the background (load it from load_img)
    :param x: the x position in which to paste the image
    :param y: the y position in which to paste the image
    """
    background_img.paste(img_to_paste, (int(x), int(y)), img_to_paste)


def draw_text_on_img(img, text, x, y, hex_color, path_to_font, font_size, anchor='lm'):
    """Will draw text on a given image.

    NOTICE: if you got a problem with the text direction, do all these:
      pip uninstall pillow           # remove existing package
      brew install libimagequant
      brew install zlib
      brew install libraqm  # for supporting hebrew and other rtl languages
      export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"
      pip3 install --upgrade Pillow --global-option="build_ext" --global-option="--enable-imagequant" --global-option="--enable-zlib" --global-option="--vendor-raqm"

    *Taken from here:
    https://stackoverflow.com/a/61969447/4036390

    Parameters:
    :param img: the img which will be served as the background to write on
    :param text: the text to write
    :param x: the x position in which to start the writing
    :param y: the y position in which to start the writing
    :param hex_color: the color of the text in hex form ("#000000")
    :param path_to_font: path to the font
    :param font_size: the size of the font
    :param anchor: the place from which to start the writing. By default, the PIL algorithm will start writing from left to right.
    For RTL, you'll probably want to use "rm" to start the writing from right to left. In addition, you'll probably want to adjust your x
    coordinate to start from the right. Read more about it here:
    https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html#text-anchors
    """
    img_draw = img
    if type(img_draw) != ImageDraw:
        img_draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(path_to_font, font_size)
    img_draw.text((x, y), text, tools.hex_to_rgb(hex_color), font=font, anchor=anchor)
    return font.getbbox(text, anchor=anchor)


def get_text_size_box(text, path_to_font, font_size, anchor='lm'):
    """Will return the size of the text you'd like to write, without writing the text

    Parameters:
    :param text: the text to calculate it's size
    :param path_to_font: path to the font
    :param font_size: the size of the font
   """
    font = ImageFont.truetype(path_to_font, font_size)
    box = font.getbbox(text, anchor=anchor)
    return box


def get_text_line_width(text, path_to_font, font_size, anchor='lm'):
    """Will return the size of the text line you'd like to write, without writing the text

    Parameters:
    :param text: the text to calculate it's size
    :param path_to_font: path to the font
    :param font_size: the size of the font
   """
    return get_text_size_box(text, path_to_font, font_size, anchor=anchor)[2]


def resize_img_by_height(img, desired_height):
    """Will resize an image by height

    Parameters:
    :param img: the img which will be resized (load it from load_img)
    :param desired_height: the image desired height
    :return resized image by height (the width will be resized by ratio)
    """
    percent_multiplier = (desired_height / float(img.size[1]))
    desired_width = int((float(img.size[0]) * float(percent_multiplier)))
    return img.resize((desired_width, desired_height), Image.ANTIALIAS)


def resize_img_by_width(img, desired_width):
    """Will resize an image by width

    Parameters:
    :param img: the img which will be resized (load it from load_img)
    :param desired_width: the image desired width
    :return resized image by width (the height will be resized by ratio)
    """
    percent_multiplier = (desired_width / float(img.size[0]))
    desired_height = int((float(img.size[1]) * float(percent_multiplier)))
    return img.resize((desired_width, desired_height), Image.ANTIALIAS)


def resize_img_by_width_and_height(img, desired_width, desired_height):
    """Will resize an image by width and height

    Parameters:
    :param img: the img which will be resized (load it from load_img)
    :param desired_width: the image desired width
    :param desired_height: the image desired height
    :return resized image by width and height
    """
    import PIL
    return img.resize((desired_width, desired_height), PIL.Image.Resampling.LANCZOS)


def save_img(img, dst, format='PNG', to_compress=False):
    """Will save the image to a given destination

    NOTICE:
      * If you want want to compress the image in mac osx, you should run all of these, one by one:
      pip uninstall pillow           # remove existing package
      brew install libimagequant
      brew install zlib
      brew install libraqm  # for supporting hebrew and other rtl languages
      export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"
      pip3 install --upgrade Pillow --global-option="build_ext" --global-option="--enable-imagequant" --global-option="--enable-zlib" --global-option="--vendor-raqm"

    *Taken from here:
    https://stackoverflow.com/a/61969447/4036390

    Parameters:
    :param img the image to save
    :param dst the path to save the file
    :param format usually png
    :param to_compress toggle to compress the file (read how to)
    """
    if to_compress:
        img.quantize(colors=256, method=3).save(dst, format)
    else:
        img.save(dst, format)


def set_gradient(width, height, color_start, color_end):
    gradient = Image.new('RGBA', (width, height), color=0)
    draw = ImageDraw.Draw(gradient)
    color_start_rgb = tools.hex_to_rgb(color_start)
    color_end_rgb = tools.hex_to_rgb(color_end)

    def interpolate(f_co, t_co, interval):
        det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
        for j in range(interval):
            yield [round(f + det * j) for f, det in zip(f_co, det_co)]

    for i, color in enumerate(interpolate(color_start_rgb, color_end_rgb, width * 2)):
        draw.line([(i, 0), (0, i)], tuple(color), width=1)
    return gradient


# will build a rectangle image. Don't forget to pase it to your main canvas at the end!
def build_rectangle_img(width, height, fill_color, outline_color, outline_width, radius):
    rectangle_image = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(rectangle_image)
    fill_color = None if fill_color is None else tools.hex_to_rgb(fill_color)
    outline_color = None if outline_color is None else tools.hex_to_rgb(outline_color)
    draw.rounded_rectangle((0, 0, width, height),
                           fill=fill_color,
                           outline=outline_color,
                           width=outline_width,
                           radius=radius)
    return rectangle_image
