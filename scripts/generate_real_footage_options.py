from __future__ import annotations
import math, subprocess
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,DUR=1280,720,24,48
SRC=Path('assets/footage/nasa/earth-observations-sample.mp4')
OUT=Path('outputs/final-look-options/2147-real-footage-options.mp4')
TMP=Path('outputs/final-look-options/2147-real-footage-options-temp.mp4')
POSTER=Path('outputs/final-look-options/2147-real-footage-options-poster.png')
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
def font(name,size):
    p=FONT_DIR/name
    return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default()
REG=lambda s:font('DejaVuSans.ttf',s); BOLD=lambda s:font('DejaVuSans-Bold.ttf',s); COND=lambda s:font('DejaVuSansCondensed-Bold.ttf',s)
INK=(7,20,38); BLUE=(15,76,129); RED=(215,25,32); WHITE=(248,250,252); MUTED=(148,163,184); GREEN=(22,163,74); ORANGE=(232,93,42); CYAN=(0,166,214); BLACK=(3,5,10)

def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3

def txt(d,xy,s,f,fill=WHITE,anchor=None,spacing=4,align='left'):
    d.multiline_text(xy,s,font=f,fill=fill,anchor=anchor,spacing=spacing,align=align)

def rr(d,box,r,fill,outline=None,width=1): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def get_frame(cap, idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ok, frame=cap.read()
    if not ok:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0); ok, frame=cap.read()
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im=Image.fromarray(frame).resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
    return im

def overlay_gradient(im, strength=.42):
    layer=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer,'RGBA')
    d.rectangle((0,0,W,H),fill=(0,0,0,int(70*strength)))
    for y in range(H):
        a=int((y/H)*150*strength)
        d.line((0,y,W,y),fill=(0,0,0,a))
    im.alpha_composite(layer)

def bug(d,compact=True):
    h=44 if compact else 54; x=42; y=34; w1=72 if compact else 88; w2=96 if compact else 112
    rr(d,(x,y,x+w1+w2+6,y+h),12,(255,255,255,0))
    d.rounded_rectangle((x,y,x+w1,y+h),radius=10,fill=(245,248,252,238))
    d.rectangle((x+w1-8,y,x+w1,y+h),fill=(245,248,252,238))
    d.rectangle((x+w1,y,x+w1+w2,y+h),fill=BLUE)
    d.rectangle((x+w1+w2,y,x+w1+w2+6,y+h),fill=RED)
    txt(d,(x+12,y+7),'2147',COND(24 if compact else 29),fill=INK)
    txt(d,(x+w1+13,y+9),'NEWS\nNETWORK',BOLD(10 if compact else 12),fill=WHITE,spacing=0)

def live_clock(d,label='LIVE'):
    rr(d,(220,36,292,72),18,RED)
    d.ellipse((234,49,242,57),fill=WHITE)
    txt(d,(250,45),label,BOLD(12),fill=WHITE)
    rr(d,(1002,36,1238,72),18,(0,0,0,145),outline=(255,255,255,45))
    txt(d,(1020,48),'18 OCT 2147 / 19:42 UTC-O',BOLD(12),fill=(220,235,246))

def ticker(d,label='HEADLINES', text='MARS TURNOUT 91% • EARTH UNION HEARING • HELION GRID WARNING • '):
    rr(d,(22,642,1258,698),14,(3,5,10,232),outline=(255,255,255,28))
    d.rounded_rectangle((22,642,206,698),radius=14,fill=RED)
    d.rectangle((190,642,206,698),fill=RED)
    txt(d,(68,661),label,BOLD(14),fill=WHITE)
    msg=(text*4)
    txt(d,(228,661),msg,BOLD(16),fill=(235,240,248))

def strap(d,label,headline,sub,tag='LIVE 2147',breaking=False):
    y=552
    rr(d,(22,y,1258,y+86),14,(255,255,255,242),outline=(255,255,255,55))
    d.rounded_rectangle((22,y,206,y+86),radius=14,fill=RED if breaking else BLUE)
    d.rectangle((190,y,206,y+86),fill=RED if breaking else BLUE)
    txt(d,(70,y+31),label.upper(),BOLD(14),fill=WHITE)
    txt(d,(228,y+10),headline.upper(),COND(38),fill=INK)
    txt(d,(230,y+51),sub,BOLD(13),fill=(83,96,113))
    d.rectangle((1108,y,1258,y+86),fill=(232,237,245))
    txt(d,(1130,y+27),tag.upper(),BOLD(11),fill=INK)

def source(d,text,x=860,y=105):
    rr(d,(x,y,x+360,y+40),20,(0,0,0,150),outline=(255,255,255,45))
    d.rounded_rectangle((x,y,x+88,y+40),radius=20,fill=RED)
    d.rectangle((x+70,y,x+88,y+40),fill=RED)
    txt(d,(x+18,y+13),'SOURCE',BOLD(10),fill=WHITE)
    txt(d,(x+105,y+12),text,BOLD(12),fill=(230,238,246))

def option_label(d,letter,title):
    rr(d,(42,96,250,136),20,(0,166,214,42),outline=(0,166,214,105))
    txt(d,(60,109),f'OPTION {letter}',BOLD(13),fill=(210,245,255))
    txt(d,(42,146),title.upper(),COND(52),fill=WHITE)

def draw_option_a(im,t):
    d=ImageDraw.Draw(im,'RGBA'); overlay_gradient(im,.72); bug(d); live_clock(d); option_label(d,'A','Clean Global News')
    source(d,'NASA Public Domain Footage')
    strap(d,'Breaking','Earth Union prepares sovereignty hearing','Stock footage full-screen with clean broadcast overlay',breaking=True)
    ticker(d,'HEADLINES','MARS VOTE • EARTH UNION HEARING • ENERGY CONTRACT RISK • ')
    return im

def draw_option_b(im,t):
    # make studio over dark background, put video as wall
    bg=Image.new('RGBA',(W,H),(5,8,15,255)); d=ImageDraw.Draw(bg,'RGBA')
    for x in range(0,W,80): d.line((x,100,x,620),fill=(255,255,255,14))
    for y in range(120,620,70): d.line((0,y,W,y),fill=(255,255,255,10))
    bug(d,False); live_clock(d)
    # video wall
    wall=im.crop((0,0,W,H)).resize((620,350),Image.Resampling.LANCZOS)
    mask=Image.new('L',(620,350),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,620,350),radius=28,fill=255)
    bg.paste(wall,(600,120),mask)
    d.rounded_rectangle((600,120,1220,470),radius=28,outline=(255,255,255,70),width=2)
    txt(d,(632,152),'MARS\nREFERENDUM\nVISUAL FEED',COND(50),fill=WHITE,spacing=-3)
    # anchor silhouette
    d.ellipse((188,205,278,295),fill=(225,235,245,160))
    d.rounded_rectangle((145,310,325,515),radius=56,fill=(255,255,255,42),outline=(255,255,255,55))
    d.rounded_rectangle((80,520,470,602),radius=36,fill=(255,255,255,32),outline=(255,255,255,52))
    strap(d,'Studio','Anchor leads with large video wall','Best for intros and live analysis')
    # lower third above ticker
    rr(d,(58,468,520,542),12,(255,255,255,240))
    d.rounded_rectangle((58,468,180,542),radius=12,fill=BLUE); d.rectangle((165,468,180,542),fill=BLUE)
    txt(d,(88,494),'ANCHOR',BOLD(12),fill=WHITE); txt(d,(198,480),'ANAYA RAO',COND(30),fill=INK); txt(d,(200,514),'Senior Anchor • Earth-Orbit Media Ring',BOLD(12),fill=(83,96,113))
    ticker(d,'HEADLINES','STUDIO VIDEO WALL • LIVE ANALYSIS • MARS DATA FEED • ')
    return bg

def draw_option_c(im,t):
    # Apple-clean map/report hybrid with video softly visible
    im=im.filter(ImageFilter.GaussianBlur(1.5)); overlay_gradient(im,.45); d=ImageDraw.Draw(im,'RGBA'); bug(d); option_label(d,'C','Apple-Clean Premium')
    rr(d,(70,185,590,440),28,(255,255,255,235),outline=(255,255,255,80))
    txt(d,(105,220),'ROUTE ANALYSIS',BOLD(13),fill=BLUE)
    txt(d,(105,250),'Earth–Mars\nCorridor',COND(62),fill=INK,spacing=-4)
    txt(d,(105,372),'Cargo insurance and treaty risk now affect long-range infrastructure contracts.',REG(20),fill=(83,96,113))
    rr(d,(745,155,1170,410),30,(255,255,255,55),outline=(255,255,255,80))
    # route line inside glass
    d.line((800,315,1110,230),fill=(255,255,255,170),width=4)
    d.ellipse((790,305,812,327),fill=RED); d.ellipse((1100,220,1122,242),fill=RED)
    rr(d,(795,452,1160,538),24,(255,255,255,235))
    txt(d,(820,468),'+18.6%',COND(46),fill=INK); txt(d,(960,482),'CARGO INSURANCE RISK',BOLD(13),fill=(83,96,113))
    strap(d,'Analysis','Interplanetary route risk rises','Premium map/explainer treatment')
    ticker(d,'MARKETS','EARTH-MARS CORRIDOR • CERES CARGO DELAYS • MARS INFRA BONDS −4.2% • ')
    return im

def draw_option_d(im,t):
    bg=Image.new('RGBA',(W,H),(4,8,15,255)); d=ImageDraw.Draw(bg,'RGBA')
    for x in range(0,W,56): d.line((x,80,x,625),fill=(255,255,255,14))
    for y in range(100,625,56): d.line((0,y,W,y),fill=(255,255,255,10))
    bug(d); live_clock(d,'DATA'); option_label(d,'D','Data-Heavy Board')
    rr(d,(64,190,590,526),26,(255,255,255,238)); txt(d,(98,222),'FINANCIAL DESK',BOLD(13),fill=GREEN); txt(d,(98,252),'Energy Markets\nWatch Mars Vote',COND(56),fill=INK,spacing=-3); txt(d,(98,372),'Helion Grid Systems warns unresolved treaty language could delay fusion-grid contracts.',REG(19),fill=(83,96,113))
    metrics=[('+18.6%','Cargo Insurance'),('14 mo.','Contract Risk'),('−4.2%','Mars Bonds')]
    for i,(v,l) in enumerate(metrics):
        x=650+i*185; rr(d,(x,210,x+165,300),16,(255,255,255,238)); txt(d,(x+15,226),v,COND(34),fill=INK); txt(d,(x+15,266),l.upper(),BOLD(10),fill=(83,96,113))
    rr(d,(650,335,1200,520),20,(255,255,255,35),outline=(255,255,255,55))
    pts=[(680,480),(760,438),(840,450),(930,380),(1030,410),(1165,355)]
    d.line(pts,fill=GREEN,width=5)
    strap(d,'Markets','Cargo insurance rises as treaty risk widens','Bloomberg-style data board for finance and elections')
    ticker(d,'MARKETS','HELION GRID SYSTEMS • CARGO INSURANCE +18.6% • CONTRACT RISK 14 MONTHS • ')
    return bg

def main():
    cap=cv2.VideoCapture(str(SRC)); frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1000
    OUT.parent.mkdir(parents=True,exist_ok=True)
    writer=cv2.VideoWriter(str(TMP),cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
    for n in range(FPS*DUR):
        t=n/FPS; idx=(n*2)%frames; im=Image.fromarray(cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)).resize((W,H)).convert('RGBA') if False else None
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx); ok, fr=cap.read()
        if not ok: cap.set(cv2.CAP_PROP_POS_FRAMES,0); ok,fr=cap.read()
        im=Image.fromarray(cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)).resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
        sec=int(t//12)
        local=t-sec*12
        if sec==0: out=draw_option_a(im,t)
        elif sec==1: out=draw_option_b(im,t)
        elif sec==2: out=draw_option_c(im,t)
        else: out=draw_option_d(im,t)
        # fades
        fade=min(1, local/.45, (12-local)/.45)
        if fade<1: out=Image.blend(Image.new('RGBA',(W,H),(5,7,13,255)),out,ease(fade))
        if n==FPS*2: out.convert('RGB').save(POSTER)
        writer.write(cv2.cvtColor(np.array(out.convert('RGB')),cv2.COLOR_RGB2BGR))
        if n%(FPS*6)==0: print('frame',n,'/',FPS*DUR)
    writer.release(); cap.release()
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.check_call([ff,'-y','-i',str(TMP),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart','-preset','medium','-crf','22',str(OUT)])
    TMP.unlink(missing_ok=True)
    print('wrote',OUT)
if __name__=='__main__': main()
