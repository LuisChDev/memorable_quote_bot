# where the image is made.

from PIL import Image, ImageDraw, ImageFont
from imgurpython import ImgurClient
from textwrap import wrap
from urllib.parse import urlparse
import random
import os
from imgur_secret import client_id, client_secret

size = 220, 260
# gurClient = []
# with open('imgur_secret.yml', 'r') as secrets:
#     gurClient = yaml.load(secrets)

# 0. connects to imgur ("client_id", "client_secret")
gur = ImgurClient(client_id, client_secret)


def delete_image(image_name):
    """
    deletes image based on link.
    """
    image_id = os.path.splitext(urlparse(image_name).path)[0].replace('/', '')
    gur.delete_image(image_id)


# function that takes a quote and uploads a randomly generated "inspirational"
# quote
def build_image(quote, img_name, person):
    # 0. generates empty new img
    img = Image.new("RGBA", (600, 300), (0, 0, 0))
    print('generated empty image.')

    # 1. select a random image from the archive
    # with open('historical_figures.txt') as figures:
    #     randompic = int(random.random()*66)
    #     name = figures.read().split('\n')[randompic]
    pic = Image.open('images/'+person+'.jpg')
    #     signature = Image.open('signatures/'+name+'.png')

    # 1.1. automatically generate signature from name
    # 1.1.1. generate the image and the font
    sig = Image.new("RGBA", (320, 30), (0, 0, 0))
    fuente = ImageFont.truetype("DejaVuSerif.ttf", 25)

    # 1.1.2. draw the signature in
    draw = ImageDraw.Draw(sig)
    draw.text((0, 2), '~'+person, (255, 255, 255), font=fuente)
    del draw

    # 2.1. calculate offset from corner so that the image is centered
    print(str(pic.width)+' '+str(pic.height))
    x_off = int((220 - pic.width) / 2) + 10
    y_off = int((260 - pic.height) / 2) + 20
    print(str(x_off)+' '+str(y_off))

    # 2.2. paste it on top of the new one
    img.paste(pic, (x_off, y_off, x_off + pic.width, y_off + pic.height))
    img.paste(sig, (260, 250, 580, 280))
    print('pasted succesfully.')

    # 2. select font
    quote_font = ImageFont.truetype('DejaVuSerif.ttf', 25)
    print('quote has been selected.')

    # 3. add the text to image, making sure it wraps around the text area
    draw = ImageDraw.Draw(img)
    draw.text((260, 20), '\n'.join(wrap(quote, width=25)),
              (255, 255, 255), font=quote_font)
    del draw
    print('quote has been added.')

    img.save('generated/'+img_name+'.png')

    # 4. upload it to imgur:
    config = {
        'album': None,
        'name': 'a random piece of history',
        'title': 'a random piece of history',
        }
    ret = gur.upload_from_path('generated/'+img_name+'.png', config=config,
                               anon=True)

    # 5. finally, return the link
    return ret["link"]
