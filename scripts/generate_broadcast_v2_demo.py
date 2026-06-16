"""Generate a redesigned V2 broadcast-style demo video.

This is code-rendered motion graphics, not AI-generated imagery/video.
The goal is to look like an actual international TV news package rather than
abstract sci-fi UI.
"""
from __future__ import annotations
import math, subprocess
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,DUR=1280,720,24,48
OUT=Path('outputs/demo-video/2147-broadcast-v2-demo.mp4')
TMP=Path('outputs/demo-video/2147-broadcast-v2-temp.mp4')
POSTER=Path('outputs/demo-video/2147-broadcast-v2-poster.png')

FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
def f(name,size):
    p=FONT_DIR/name
    return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default()
REG=lambda s:f('DejaVuSans.ttf',s); BOLD=lambda s:f('DejaVuSans-Bold.ttf',s); COND=lambda s:f('DejaVuSansCondensed-Bold.ttf',s)
NAVY=(7,20,38); BLUE=(14,42,71); WHITE=(248,250,252); MUTED=(148,163,184); RED=(215,25,32); ORANGE=(232,93,42); CYAN=(0,166,214); GREEN=(22,163,74); BLACK=(5,7,13)

def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3

def text(d,xy,s,font,fill=WHITE,anchor=None,spacing=4,align='left'):
    d.multiline_text(xy,s,font=font,fill=fill,anchor=anchor,spacing=spacing,align=align)

def rect(d,box,fill,outline=None,w=1,r=0):
    if r: d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
    else: d.rectangle(box,fill=fill,outline=outline,width=w)

def base(t, mode='normal'):
    arr=np.zeros((H,W,3),dtype=np.uint8)
    y=np.linspace(0,1,H)[:,None]
    top=np.array((9,25,47)); bot=np.array((3,5,11))
    arr[:]=(top*(1-y)+bot*y).astype(np.uint8)[:,None,:]
    im=Image.fromarray(arr,'RGB').convert('RGBA'); d=ImageDraw.Draw(im,'RGBA')
    # studio diagonal panels
    for i in range(-200,W+400,180):
        d.polygon([(i,0),(i+80,0),(i-220,H),(i-320,H)],fill=(255,255,255,8))
    # safe subtle grid wall
    for x in range(0,W,80): d.line((x,88,x,H-92),fill=(255,255,255,10))
    for y0 in range(120,H-90,70): d.line((0,y0,W,y0),fill=(255,255,255,8))
    return im

def bug(d,t,breaking=False):
    rect(d,(28,24,116,70),(255,255,255,235),r=6)
    text(d,(42,31),'2147',BOLD(24),fill=NAVY)
    text(d,(43,54),'NEWS',BOLD(12),fill=NAVY)
    rect(d,(122,24,238,70),RED if breaking else BLUE,r=5)
    text(d,(138,34),'LIVE',BOLD(18),fill=WHITE)
    text(d,(185,37),'2147',BOLD(14),fill=(230,240,248))
    rect(d,(1040,24,1250,70),(0,0,0,125),outline=(255,255,255,35),r=6)
    text(d,(1060,35),'18 OCT 2147 / 19:42 UTC-O',BOLD(12),fill=(220,232,242))

def lower(d,title,sub='',breaking=False):
    y=560
    rect(d,(0,y,W,640),(255,255,255,235))
    rect(d,(0,y,195,640),RED if breaking else BLUE)
    text(d,(28,y+16),'BREAKING' if breaking else 'DEVELOPING',BOLD(19),fill=WHITE)
    text(d,(220,y+9),title,COND(38),fill=(5,7,13))
    if sub: text(d,(222,y+49),sub,BOLD(15),fill=(70,82,96))

def ticker(d,t):
    rect(d,(0,640,W,690),BLACK)
    rect(d,(0,640,145,690),RED)
    text(d,(28,654),'HEADLINES',BOLD(15),fill=WHITE)
    msg='MARS TURNOUT PROJECTION RISES TO 91%  •  EARTH UNION LEGAL REVIEW BEGINS  •  HELION GRID SYSTEMS WARNS OF CONTRACT RISK  •  SYNTHETIC RIGHTS TRIBUNAL RECEIVES PETITION  •  '
    tw=d.textlength(msg,font=BOLD(16)); x=160-((t*95)%(tw))
    text(d,(x,654),msg*3,BOLD(16),fill=(230,236,244))

def mars_icon(d,cx,cy,r):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=ORANGE,outline=(255,190,160),width=2)
    d.arc((cx-r+15,cy-r+45,cx+r-10,cy+r-35),200,340,fill=(120,35,25),width=10)
    d.arc((cx-r+25,cy-r+90,cx+r-20,cy+r-5),200,340,fill=(140,45,28),width=8)

def bars(d,x,y,w):
    rows=[('INDEPENDENCE',.57,GREEN),('UNION',.39,ORANGE),('UNDECIDED',.04,MUTED)]
    for i,(lab,p,col) in enumerate(rows):
        yy=y+i*55; text(d,(x,yy),lab,BOLD(15),fill=(230,236,244)); rect(d,(x+170,yy+4,x+170+w,yy+22),(42,52,66),r=10)
        rect(d,(x+170,yy+4,x+170+int(w*p),yy+22),col,r=10); text(d,(x+190+w,yy-3),f'{int(p*100)}%',BOLD(23),fill=WHITE)

def scene_cold(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t,True)
    rect(d,(0,105,W,178),RED); text(d,(42,119),'BREAKING NEWS',COND(56),fill=WHITE)
    text(d,(64,230),'MARS VOTES\nON INDEPENDENCE',COND(92),fill=WHITE,spacing=-10)
    mars_icon(d,1010,345,120)
    rect(d,(64,465,650,522),(255,255,255,230),r=6); text(d,(88,478),'FINAL VOTING CYCLE • 42 SETTLEMENT ZONES',BOLD(23),fill=NAVY)
    lower(d,'Mars referendum enters final hours','Source: Mars Civic Council Election Board',True); ticker(d,t); return im

def scene_anchor(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    # studio desk/anchor
    rect(d,(55,120,420,535),(12,31,52,220),outline=(255,255,255,35),r=10)
    d.ellipse((190,210,285,305),fill=(220,236,245,160)); d.rounded_rectangle((150,320,330,520),radius=50,fill=(225,240,248,55),outline=(255,255,255,45))
    rect(d,(440,120,1225,535),(9,28,49,230),outline=(255,255,255,40),r=10)
    text(d,(480,150),'MARS REFERENDUM',BOLD(20),fill=CYAN); text(d,(480,190),'Final Voting\nCycle Begins',COND(70),spacing=-8)
    bars(d,480,370,430); mars_icon(d,1050,305,95)
    lower(d,'ANAYA RAO','Senior Anchor • Earth-Orbit Media Ring'); ticker(d,t); return im

def scene_board(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    text(d,(48,105),'TOP STORIES',COND(54)); cards=[('MARS VOTE','Independence model shows 57% support',ORANGE),('EARTH UNION','Emergency sovereignty hearing expected',RED),('MARKETS','Jiang Lau warns of contract delays',GREEN),('TRIBUNAL','AI voting-rights petition filed',CYAN)]
    for i,(a,b,c) in enumerate(cards):
        x=60+(i%2)*610; y=185+(i//2)*165
        rect(d,(x,y,x+560,y+130),(255,255,255,235),r=8); rect(d,(x,y,x+12,y+130),c)
        text(d,(x+35,y+22),a,BOLD(24),fill=NAVY); text(d,(x+35,y+62),b,REG(25),fill=(35,45,58))
    lower(d,'Mars sovereignty crisis widens','Four linked developments now active'); ticker(d,t); return im

def scene_data(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    text(d,(48,105),'MARS REFERENDUM DATA BOARD',COND(47)); rect(d,(55,170,1215,535),(8,23,41,235),outline=(255,255,255,35),r=10)
    stats=[('38.2M','MARS POPULATION'),('29.4M','ELIGIBLE VOTERS'),('91%','PROJECTED TURNOUT')]
    for i,(v,k) in enumerate(stats):
        x=90+i*365; rect(d,(x,205,x+315,305),(255,255,255,235),r=8); text(d,(x+25,222),v,COND(50),fill=NAVY); text(d,(x+25,278),k,BOLD(15),fill=(70,82,96))
    bars(d,120,365,720); text(d,(925,380),'SOURCE\nMars Civic Council\nElection Board',BOLD(22),fill=(220,232,242),spacing=7)
    lower(d,'Independence model leads at 57%','Provisional settlement model • 19:42 UTC-Orbital'); ticker(d,t); return im

def scene_timeline(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    text(d,(48,105),'HOW WE GOT HERE',COND(55)); rect(d,(70,190,1210,500),(255,255,255,235),r=10)
    pts=[('2136','Oxygen-credit protests'),('2142','Cargo tariff challenge'),('2147','Final voting cycle'),('NEXT','Legal & market ripples')]
    d.line((160,335,1100,335),fill=(70,82,96),width=4)
    for i,(yr,desc) in enumerate(pts):
        x=160+i*310; d.ellipse((x-15,320,x+15,350),fill=RED if i==2 else BLUE)
        text(d,(x,235),yr,COND(40),fill=NAVY,anchor='ma'); text(d,(x-95,365),desc,BOLD(20),fill=(35,45,58),align='center')
    lower(d,'Referendum follows decades of off-world disputes','Timeline Archive • 2147 News Network'); ticker(d,t); return im

def scene_split(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    rect(d,(55,120,610,535),(255,255,255,235),r=10); rect(d,(640,120,1225,535),(255,255,255,235),r=10)
    text(d,(85,150),'EXPERT ANALYSIS',BOLD(19),fill=BLUE); d.ellipse((260,205,400,345),fill=(190,205,218)); text(d,(110,385),'DR. ILYAN SEN',COND(38),fill=NAVY); text(d,(112,430),'Political Historian\nUniversity of Valles Marineris',BOLD(20),fill=(65,78,92))
    text(d,(675,155),'“Mars is no longer\nan outpost. It is a\ncivilization asking for\npolitical recognition.”',COND(46),fill=NAVY,spacing=0)
    lower(d,'Expert: Mars is asking for political recognition','Archive Feed • University of Valles Marineris'); ticker(d,t); return im

def scene_finance(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    text(d,(48,105),'FINANCIAL DESK',COND(55)); rect(d,(55,170,580,535),(255,255,255,235),r=10); rect(d,(610,170,1215,535),(8,23,41,235),outline=(255,255,255,35),r=10)
    text(d,(90,205),'JIANG LAU',COND(42),fill=NAVY); text(d,(92,255),'CEO • Helion Grid Systems',BOLD(19),fill=(65,78,92)); text(d,(90,315),'“Energy markets can absorb\npolitical change. They cannot\nabsorb legal uncertainty.”',REG(30),fill=(20,30,44),spacing=5)
    metrics=[('+18.6%','Cargo Insurance'),('14 mo.','Contract Risk'),('−4.2%','Mars Bonds')]
    for i,(v,k) in enumerate(metrics):
        x=650+i*180; rect(d,(x,210,x+155,290),(255,255,255,230),r=8); text(d,(x+15,225),v,COND(33),fill=NAVY); text(d,(x+15,263),k.upper(),BOLD(11),fill=(70,82,96))
    pts=[(660,465),(730,430),(820,450),(900,370),(990,400),(1080,315),(1170,340)]; d.line(pts,fill=GREEN,width=5)
    lower(d,'Energy markets watch Mars vote','Outer Belt Trade Registry • Singapore Arcology Financial Feed'); ticker(d,t); return im

def scene_legal(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    text(d,(48,105),'LEGAL DESK',COND(55)); rect(d,(55,170,640,535),(255,255,255,235),r=10); rect(d,(670,170,1215,535),(255,255,255,235),r=10)
    text(d,(90,205),'AI VOTING RIGHTS\nPETITION FILED',COND(48),fill=NAVY,spacing=-4); text(d,(92,320),'Synthetic Rights Tribunal receives certification petition over memory-continuity residents.',REG(26),fill=(35,45,58))
    stats=[('42','Zones'),('3.8M','Residents'),('Pending','Jurisdiction'),('2147-CV','Case')]
    for i,(v,k) in enumerate(stats):
        x=705+(i%2)*235; y=205+(i//2)*115; rect(d,(x,y,x+195,y+85),(12,31,52,235),r=8); text(d,(x+18,y+14),v,COND(33)); text(d,(x+18,y+55),k.upper(),BOLD(12),fill=MUTED)
    lower(d,'Tribunal receives Mars referendum petition','Synthetic Rights Tribunal • Geneva Continuity Court Complex'); ticker(d,t); return im

def scene_close(t,l):
    im=base(t); d=ImageDraw.Draw(im,'RGBA'); bug(d,t)
    text(d,(W//2,210),'NEXT ON 2147 NEWS',COND(58),anchor='ma')
    rect(d,(210,295,1070,410),RED,r=8); text(d,(W//2,318),'EARTH UNION HEARING',COND(54),anchor='ma')
    text(d,(W//2,455),'For Earth, Luna, Mars, and the Outer Belt — End Transmission.',BOLD(26),fill=(225,234,242),anchor='ma')
    lower(d,'End Transmission','Broadcast Archive Saved'); ticker(d,t); return im

SC=[(0,5,scene_cold),(5,11,scene_anchor),(11,16,scene_board),(16,22,scene_data),(22,27,scene_timeline),(27,32,scene_split),(32,38,scene_finance),(38,43,scene_legal),(43,48,scene_close)]
def frame(n):
    t=n/FPS
    for a,b,fn in SC:
        if a<=t<b:
            im=fn(t,(t-a)/(b-a)); fade=min(1,(t-a)/.3,(b-t)/.3)
            if fade<1: im=Image.blend(Image.new('RGBA',(W,H),(3,5,11,255)),im,ease(fade))
            return im.convert('RGB')
    return scene_close(t,1).convert('RGB')

def transcode(src,dst):
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.check_call([ff,'-y','-i',str(src),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart','-preset','medium','-crf','22',str(dst)])

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    writer=cv2.VideoWriter(str(TMP),cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
    for n in range(FPS*DUR):
        im=frame(n)
        if n==FPS*2: im.save(POSTER)
        writer.write(cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR))
        if n%(FPS*6)==0: print('frame',n,'/',FPS*DUR)
    writer.release(); transcode(TMP,OUT); TMP.unlink(missing_ok=True)
    print('wrote',OUT)
if __name__=='__main__': main()
