# from PIL import Image
# im = Image.open("z.png")
# # im.show()
# print(im.format, im.size, im.mode)
# # PNG (1080, 2160) RGB

from PIL import Image
im = Image.open('z.png')
pix = im.load()
width = im.size[0]
height = im.size[1]
# x     y
# a=(840,   1380)
# b=(860,   1450)
# c=(990,   1580)
# d=(1010,  1640)

p1 = (990, 1380)
p2 = (835, 1580)
for x in range(990, 1010):
  for y in range(1380, 1450):
    r,g,b = im.getpixel((x,y))    
    rgba=(r,g,b)
    # 矩形内像素值替换
    im.putpixel( (p1[0]+x-p1[0], p1[1]+y-p1[1]), rgba)

# 定位坐标/划红线
    # if( x == 840 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))
    # if( x == 860 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))
    # if( x == 990 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))
    # if( x == 1010 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))


    # if( y == 1580 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))
    # if( y == 1640 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))
    # if( y == 1380 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))
    # if( y == 1450 ):
    #     r,g,b = im.getpixel((x,y))    
    #     rgba=(r,g,b)
    #     im.putpixel((x,y), (255, 20, 147))


im = im.convert('RGB')
im.save('zz.png')
im.show()

