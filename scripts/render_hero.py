"""Rebuild the profile's code-to-landscape animation. Requires Pillow 13.0.0.
Run from repository root: python scripts/render_hero.py
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, random
W,H=1000,360
OUT=Path(__file__).resolve().parents[1]/'assets'
OUT.mkdir(exist_ok=True)
FONT=Path('/usr/share/fonts/truetype/dejavu')
def font(n,bold=False,mono=False):
    name='DejaVuSansMono.ttf' if mono else ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')
    return ImageFont.truetype(str(FONT/name),n)
def ease(x):
    x=max(0,min(1,x)); return x*x*(3-2*x)
def mix(a,b,t):return tuple(round(x+(y-x)*t) for x,y in zip(a,b))
bg=(12,23,26); cream=(239,234,218); teal=(111,171,158)
random.seed(7)
points=[]
for i in range(210):
    x=520+random.random()*455
    ridge=220-100*math.exp(-((x-745)/76)**2)-50*math.exp(-((x-920)/55)**2)
    points.append((530+(i%34)*12,105+(i//34)*22,x,ridge+random.random()*4,random.random()))
def frame(t):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    # restrained editorial framing; identity is readable even before animation loads
    d.line((32,44,968,44),fill=(46,64,65)); d.line((32,321,968,321),fill=(46,64,65))
    d.text((34,19),'HEW / INDEPENDENT BUILDER',font=font(11,mono=True),fill=teal)
    d.text((819,19),'CODE INTO POETRY',font=font(10,mono=True),fill=(146,157,151))
    d.text((29,76),'HEW',font=font(100,bold=True),fill=cream)
    d.ellipse((292,158,305,171),fill=(210,91,69))
    d.text((35,201),'Useful tools.',font=font(26),fill=cream)
    d.text((35,236),'Thoughtful experiences.',font=font(26),fill=cream)
    d.text((35,291),'FRONTEND  /  AI  /  CREATIVE CODING',font=font(10,mono=True),fill=(138,157,152))
    d.text((35,335),'REACT + TYPESCRIPT + CURIOSITY',font=font(10,mono=True),fill=(117,143,139))
    d.text((800,335),'github.com/Hew007',font=font(10,mono=True),fill=(117,143,139))
    p=ease((t-1.1)/2.6)
    # dissolve code into three layered ridgelines
    lines=['const scene = createWorld();','scene.add(mountains);','scene.add(water, moonlight);','render({ curiosity: true });']
    for k,line in enumerate(lines):
        d.text((529,107+k*26),line,font=font(12,mono=True),fill=mix(bg,teal,(1-p)*.8))
    for j,(cy,amp,col) in enumerate([(223,87,(33,61,62)),(239,79,(41,78,76)),(258,53,(53,100,93))]):
        pts=[]
        for x in range(495,1001,3):
            y=cy-amp*math.exp(-((x-(740+j*65))/(69-j*5))**2)-amp*.55*math.exp(-((x-965)/(53+j*5))**2)+4*math.sin(x*.027+j)
            pts.append((x,y))
        d.polygon(pts+[(1000,291),(495,291)],fill=mix(bg,col,p))
        d.line(pts,fill=mix(bg,(91,142,130),p*.5),width=1)
    d.ellipse((871,77,906,112),fill=mix(bg,cream,p*.85))
    for sx,sy,ex,ey,r in points:
        q=ease((t-1.0-r*.5)/2.8)
        x=sx+(ex-sx)*q; y=sy+(ey-sy)*q-28*math.sin(q*math.pi)
        a=(.3+.5*math.sin(r*9+t*2)**2)*(1-.8*q)
        d.ellipse((x,y,x+1,y+1),fill=mix(bg,teal,a))
    # slow water glints; small boat gives the scene human scale
    for i in range(14):
        y=267+i*3; x=630+((i*67)%320)+5*math.sin(t*1.3+i)
        d.line((x,y,min(978,x+10+(i%4)*9),y),fill=mix(bg,teal,p*(.10+.09*math.sin(t+i)**2)))
    y=279+math.sin(t*1.4)*1.2
    d.polygon([(749,y),(788,y),(781,y+5),(759,y+5)],fill=mix(bg,cream,p*.85))
    d.line((769,y,769,y-12),fill=mix(bg,cream,p*.8),width=2)
    d.ellipse((766,y-17,771,y-12),fill=mix(bg,cream,p*.8))
    d.line((771,y-6,798,y+2),fill=mix(bg,cream,p*.7))
    d.text((534,67),'01 / A WORLD, WRITTEN IN CODE',font=font(10,mono=True),fill=(105,138,132))
    # Feather the illustration into the background, avoiding a rectangular panel.
    for x in range(495,565):
        a=ease((x-495)/70)
        for y in range(90,315):
            im.putpixel((x,y),mix(bg,im.getpixel((x,y)),a))
    return im
# Play once, then retain the quiet completed landscape. No endless flashing loop.
frames=[frame(i/12) for i in range(84)]
palette=frames[-1].quantize(colors=96,method=Image.Quantize.MEDIANCUT)
frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
frames[0].save(OUT/'code-into-poetry.gif',save_all=True,append_images=frames[1:],duration=[80]*83+[1000],optimize=True,disposal=1)
frame(6.9).save(OUT/'code-into-poetry.png')
print('GIF bytes:',(OUT/'code-into-poetry.gif').stat().st_size)
