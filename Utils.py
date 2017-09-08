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

def remove_from_list(target_list, removee):
    """
    utility function to remove single lines from lists. params: local directory of
the file, string to be removed.
    """
    try:
        list_file = open(target_list, 'r')
        old_list = list_file.readlines()
        list_file.figures.close()
        new_list = []
        for line in old_list:
            if line != removee+'\n':
                new_list.append(line)
        list_file = open(target_list, 'w')
        list_file.writelines(new_list)
        list_file.close()
    except Exception as e:
        print(target_list+'maybe, maybe not exists. or remove_from_list did not work. '+e)

def add_to_list(target_list, addee):
    """
    appends the given string to the given list. params: local dir of list, string
    """
    try:
        with open(target_list, 'a') as list_file:
            list_file.write(addee+'\n')
    except Exception as e:
        print(target_list+' does not seem to exist. or add_to_list didnt work.')

def get_list(target_list):
    """
    returns the list specified by local directory.
    """
    try:
        with open(target_list, 'r') as list_file:
            list_object = list_file.read().split('\n')
    except Exception as e:
        print(target_list+' does not seem to exist. or get_list didnt work.')
        return []
    return list_object
              
if __name__ == '__main__':
    prompt = input('sigs, addpic or removepic? ')
    
    if prompt == 'sigs':
        with open('historical_figures.txt') as figures:
            for someone in figures.read().split('\n'):
                makeSig(someone)

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
        new_figures = []
        for line in old_figures:
            if line != remove+'\n':
                new_figures.append(line)
        figures = open('historical_figures.txt', 'w')
        figures.writelines(new_figures)
        figures.close()
        os.remove('images/'+remove)

    else:
        print(
            "Image utils for memorable_quote_bot.\n\
              1. 'sigs': regenerates the signatures from the file.\n\
              2. 'removepic': removes a person. params: name.\n\
              3. 'addpic': adds a new person. params: image's location, name."\
            )
