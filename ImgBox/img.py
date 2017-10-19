import sys
from PIL import Image, ImageDraw

im = Image.open("22.png")

# draw = ImageDraw.Draw(im)
# draw.line((0, 0) + im.size, fill=128)
# draw.line((0, im.size[1], im.size[0], 0), fill=128)
# del draw
region = Image.open('2.jpg').resize((20,24))
x,y = int(0.97*im.width),int(0.35*im.height)

im.paste(region,(x,y))
# write to stdout

im.save('suyf.png', "PNG")