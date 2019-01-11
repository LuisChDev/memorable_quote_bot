# testing and adjusting the image generator

from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

string = 'This is a test string. It should be used with caution. it also should be longer than 20 characters, but shorter than 140. here are 20 chars.'
fuente = ImageFont.truetype('DejaVuSerif.ttf', 25)
img = Image.new("RGBA", (600, 300), (0,0,0))

draw = ImageDraw.Draw(img)
draw.text((260,20), '\n'.join(wrap(string, width=25)), (255,255,255), font=fuente)
del draw

tinyPic = Image.open('tinyPic.png')
img.paste(tinyPic, (20, 20, 240, 280))

sigpic = Image.open('sigtest.png')
img.paste(sigpic, (260, 250, 580, 280))

img.save('image'+str(len(string))+'.png')
img.show()

