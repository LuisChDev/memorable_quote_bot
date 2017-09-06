# script to refresh the signatures and images

from PIL import Image, ImageDraw, ImageFont
import os, re

def makeSig(name):
    
    # 1. generate the image and the font
    sig = Image.new("RGBA", (320,30), (0,0,0))
    fuente = ImageFont.truetype("DejaVuSerif.ttf", 25)

    # 2. draw the signature in
    draw = ImageDraw.Draw(sig)
    draw.text((0,2), '~'+name, (255,255,255), font=fuente)
    del draw

    # 3. save
    sig.save('signatures/'+name+'.png')

# Function that turns those big pics into employable images
# Run this script on any image you want to add
def makeThumbnail(directory, name):
    img = Image.open(directory)
    img.thumbnail((220,260), Image.ANTIALIAS)
    img.save('images/'+name+'.jpg')

if __name__ == '__main__':
    prompt = input('sigs, addpic or removepic? ')
    
    if prompt == 'sigs':
        with open('historical_figures.txt') as figures:
            i = 0
            for someone in figures.read().split('\n'):
                makeSig(someone, i)
                i = i + 1

    elif prompt == 'addpic':
        directory = input('image directory: ')
        name = input('person\'s name: ')
        with open('historical_figures.txt', 'a') as figures:
            figures.write('\n'+name)
        makeThumbnail(directory, name)
        makeSig(name)

    elif prompt == 'removepic':
        figures = open('historical_figures.txt', 'r')
        old_figures = figures.readlines()
        figures.close()
        remove = input('person to remove: ')
        for line in old_figures:
            if line == remove+'\n':
                old_figures.remove(line)
        figures = open('historical_figures.txt', 'w')
        figures.writelines(old_figures)
        figures.close()
        os.remove('images/'+remove)

    else:
        print(
            "Image utils for memorable_quote_bot.\n\
              1. 'sigs': regenerates the signatures from the file.\n\
              2. 'removepic': removes a person. params: name.\n\
              3. 'addpic': adds a new person. params: image's location, name."\
            )
