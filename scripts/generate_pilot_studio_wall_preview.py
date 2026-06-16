from __future__ import annotations
import subprocess
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,DUR=1280,720,24,64
SRC=Path('static/demo-assets/earth-observations-sample.mp4')
POSTER=Path('static/demo-assets/earth-observations-sample-poster.jpg')
OUT=Path('outputs/pilot-preview/2147-pilot-studio-wall-preview.mp4')
TMP=Path('outputs/pilot-preview/2147-pilot-studio-wall-preview-temp.mp4')
POSTER_OUT=Path('outputs/pilot-preview/2147-pilot-studio-wall-preview-poster.png')
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
def font(name,size):
    p=FONT_DIR/name
    return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default()
REG=lambda s:font('DejaVuSans.ttf',s); BOLD=lambda s:font('DejaVuSans-Bold.ttf',s); COND=lambda s:font('DejaVuSansCondensed-Bold.ttf',s)
INK=(7,20,38); BLUE=(15,76,129); RED=(215,25,32); WHITE=(248,250,252); MUTED=(83,96,113); GREEN=(22,163,74); ORANGE=(232,93,42); CYAN=(0,166,214)

def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3

def txt(d,xy,s,f,fill=WHITE,anchor=None,spacing=4,align='left'):
    d.multiline_text(xy,s,font=f,fill=fill,anchor=anchor,spacing=spacing,align=align)

def rr(d,box,r,fill,outline=None,width=1):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

def get_video_frame(cap, n):
    total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1000
    cap.set(cv2.CAP_PROP_POS_FRAMES,(n*2)%total)
    ok,fr=cap.read()
    if not ok:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0); ok,fr=cap.read()
    return Image.fromarray(cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)).resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')

def base_bg():
    im=Image.new('RGBA',(W,H),(5,7,13,255)); d=ImageDraw.Draw(im,'RGBA')
    for y in range(H):
        a=y/H; col=(int(11*(1-a)+2*a),int(23*(1-a)+4*a),int(40*(1-a)+10*a),255); d.line((0,y,W,y),fill=col)
    for x in range(0,W,80): d.line((x,0,x,H),fill=(255,255,255,12))
    for y in range(0,H,80): d.line((0,y,W,y),fill=(255,255,255,10))
    return im

def bug(d, live='LIVE', clock='18 OCT 2147 / 19:42 UTC-O'):
    rr(d,(46,34,252,88),12,(255,255,255,245)); d.rectangle((134,34,246,88),fill=BLUE); d.rectangle((246,34,252,88),fill=RED)
    txt(d,(58,43),'2147',COND(29),fill=INK); txt(d,(150,44),'NEWS\nNETWORK',BOLD(12),spacing=0)
    rr(d,(264,42,350,80),19,RED); d.ellipse((278,55,286,63),fill=WHITE); txt(d,(296,51),live,BOLD(12))
    rr(d,(1002,42,1238,80),19,(0,0,0,145),outline=(255,255,255,45)); txt(d,(1020,54),clock,BOLD(12),fill=(220,235,246))

def ticker(d,label='HEADLINES',text='MARS TURNOUT PROJECTED AT 91% • EARTH UNION LEGAL REVIEW BEGINS •'):
    rr(d,(20,646,1260,704),14,(3,5,10,235),outline=(255,255,255,35)); rr(d,(20,646,204,704),14,RED); d.rectangle((188,646,204,704),fill=RED)
    txt(d,(62,666),label,BOLD(14)); txt(d,(230,665),text*3,BOLD(17),fill=WHITE)

def strap(d,label,headline,sub,tag='LIVE 2147',breaking=False):
    y=552; rr(d,(22,y,1258,y+86),14,(255,255,255,245),outline=(255,255,255,50)); rr(d,(22,y,206,y+86),14,RED if breaking else BLUE); d.rectangle((190,y,206,y+86),fill=RED if breaking else BLUE)
    txt(d,(64,y+31),label.upper(),BOLD(14)); txt(d,(228,y+10),headline.upper(),COND(38),fill=INK); txt(d,(230,y+51),sub,BOLD(13),fill=MUTED)
    d.rectangle((1108,y,1258,y+86),fill=(232,237,245)); txt(d,(1132,y+27),tag.upper(),BOLD(11),fill=INK)

def lower(d,role='ANCHOR',name='ANAYA RAO',title='Senior Anchor • Earth-Orbit Media Ring',loc='STUDIO'):
    rr(d,(60,552,1220,638),14,(255,255,255,245)); rr(d,(60,552,210,638),14,BLUE); d.rectangle((195,552,210,638),fill=BLUE)
    txt(d,(96,584),role,BOLD(13)); txt(d,(232,564),name,COND(34),fill=INK); txt(d,(234,603),title,BOLD(14),fill=MUTED)
    d.rectangle((1030,552,1220,638),fill=(232,237,245)); txt(d,(1080,585),loc,BOLD(12),fill=INK)

def source(d,text,x=840,y=140):
    rr(d,(x,y,x+370,y+40),20,(0,0,0,155),outline=(255,255,255,45)); rr(d,(x,y,x+88,y+40),20,RED); d.rectangle((x+70,y,x+88,y+40),fill=RED)
    txt(d,(x+18,y+13),'SOURCE',BOLD(10)); txt(d,(x+105,y+12),text,BOLD(12),fill=(230,238,246))

def anchor_panel(d):
    left=(54,112,444,518); rr(d,left,30,(8,22,38,235),outline=(255,255,255,55))
    cx=249
    rr(d,(86,430,412,504),36,(255,255,255,36),outline=(255,255,255,70))
    rr(d,(cx-110,250,cx+110,455),65,(230,238,248,230),outline=(255,255,255,130)); d.polygon([(cx,250),(cx+48,455),(cx-48,455)],fill=(7,20,38,240))
    rr(d,(cx-24,218,cx+24,260),12,(202,149,115,255)); rr(d,(cx-52,128,cx+52,232),45,(232,197,174,255),outline=(255,255,255,120)); rr(d,(cx-60,116,cx+60,168),30,(17,24,39,255))
    rr(d,(82,332,416,430),22,(248,250,252,245),outline=(255,255,255,120)); txt(d,(106,352),'ANCHOR DESK',BOLD(11),fill=BLUE); txt(d,(106,371),'ANAYA RAO',COND(38),fill=INK); txt(d,(107,410),'Senior Anchor • Earth-Orbit Media Ring',BOLD(13),fill=MUTED)

def wall_base(im, footage=None):
    d=ImageDraw.Draw(im,'RGBA'); right=(468,112,1226,518); rr(d,right,30,(8,22,38,235),outline=(255,255,255,55))
    if footage is not None:
        crop=footage.resize((right[2]-right[0],right[3]-right[1]),Image.Resampling.LANCZOS); im.alpha_composite(crop,(right[0],right[1])); d.rounded_rectangle(right,30,fill=(0,0,0,75))
    return right

def studio_layout(footage, headline, summary, metric='91%', metric_label='Projected Turnout', label='Mars Political Desk'):
    im=base_bg(); d=ImageDraw.Draw(im,'RGBA'); bug(d); anchor_panel(d); wall_base(im,footage); d=ImageDraw.Draw(im,'RGBA')
    source(d,'NASA public domain sample')
    txt(d,(505,148),label.upper(),BOLD(13),fill=(191,239,255)); txt(d,(505,184),headline.upper(),COND(62),spacing=-6)
    txt(d,(507,382),summary,BOLD(19),fill=(219,234,254))
    rr(d,(872,385,1170,486),24,(248,250,252,240),outline=(255,255,255,120)); txt(d,(900,404),metric,COND(58),fill=INK); txt(d,(1008,425),metric_label.upper(),BOLD(13),fill=MUTED)
    lower(d); ticker(d); return im

def cold_open(footage):
    im=footage.copy(); d=ImageDraw.Draw(im,'RGBA'); d.rectangle((0,0,W,H),fill=(0,0,0,90)); bug(d,'LIVE');
    txt(d,(70,145),'BREAKING',BOLD(22),fill=(255,190,190)); txt(d,(70,190),'MARS VOTES\nON INDEPENDENCE',COND(88),spacing=-10)
    strap(d,'Breaking','Mars referendum enters final hours','Earth Union officials prepare emergency legal review',breaking=True); ticker(d); return im

def data_wall():
    im=base_bg(); d=ImageDraw.Draw(im,'RGBA'); bug(d,'DATA'); anchor_panel(d); wall_base(im); d=ImageDraw.Draw(im,'RGBA')
    rr(d,(500,145,1190,490),28,(248,250,252,240)); txt(d,(535,175),'REFERENDUM DATA BOARD',BOLD(13),fill=BLUE); txt(d,(535,205),'INDEPENDENCE\nMODEL LEADS',COND(56),fill=INK,spacing=-4)
    stats=[('38.2M','POPULATION'),('29.4M','ELIGIBLE VOTERS'),('91%','PROJECTED TURNOUT')]
    for i,(v,l) in enumerate(stats):
        x=535+i*205; rr(d,(x,335,x+180,415),18,(7,20,38,235)); txt(d,(x+16,350),v,COND(32)); txt(d,(x+16,390),l,BOLD(9),fill=(203,213,225))
    lower(d); ticker(d,'DATA','INDEPENDENCE 57% • UNION 39% • UNDECIDED 4% • '); return im

def map_wall():
    im=base_bg(); d=ImageDraw.Draw(im,'RGBA'); bug(d,'MAP'); anchor_panel(d); right=wall_base(im); d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle(right,30,fill=(238,246,252,240),outline=(255,255,255,55))
    for x in range(520,1180,56): d.line((x,140,x,490),fill=(7,20,38,25))
    for y in range(150,500,56): d.line((500,y,1190,y),fill=(7,20,38,22))
    d.line((590,385,1070,250),fill=RED,width=5); d.ellipse((578,373,602,397),fill=RED); d.ellipse((1058,238,1082,262),fill=RED)
    txt(d,(535,160),'EARTH–MARS\nCORRIDOR',COND(56),fill=INK,spacing=-4); txt(d,(535,300),'Route analysis • treaty risk • cargo insurance',BOLD(18),fill=MUTED)
    lower(d); ticker(d,'MAP','EARTH-MARS CORRIDOR • CERES CARGO DELAYS • '); return im

def quote_wall():
    im=base_bg(); d=ImageDraw.Draw(im,'RGBA'); bug(d,'ANALYSIS'); anchor_panel(d); wall_base(im); d=ImageDraw.Draw(im,'RGBA')
    rr(d,(500,145,1190,490),28,(248,250,252,240)); txt(d,(535,175),'EXPERT ANALYSIS',BOLD(13),fill=BLUE); txt(d,(535,215),'DR. ILYAN SEN',COND(54),fill=INK)
    txt(d,(535,295),'“Mars is no longer an outpost.\nIt is a civilization asking for\npolitical recognition.”',COND(42),fill=INK,spacing=3)
    lower(d,'EXPERT','DR. ILYAN SEN','Political Historian • University of Valles Marineris','ARCHIVE'); ticker(d,'ANALYSIS','UNIVERSITY OF VALLES MARINERIS • ARCHIVE FEED VERIFIED • '); return im

def archive_wall(footage):
    im=studio_layout(footage,'ARCHIVE:\nOXYGEN-CREDIT\nPROTESTS','The 2136 lunar protests turned life-support pricing into a political rights issue.','2136','Timeline Archive','Archive Feed')
    d=ImageDraw.Draw(im,'RGBA'); rr(d,(505,140,720,180),10,(0,0,0,170),outline=(255,255,255,45)); txt(d,(525,153),'ARCHIVE FOOTAGE',BOLD(13))
    ticker(d,'ARCHIVE','2136 OXYGEN-CREDIT PROTESTS • 2142 CARGO TARIFF DISPUTE • '); return im

def close_scene():
    im=base_bg(); d=ImageDraw.Draw(im,'RGBA'); bug(d,'END')
    rr(d,(170,150,1110,480),32,(248,250,252,240)); txt(d,(W//2,200),'END\nTRANSMISSION',COND(86),fill=INK,anchor='ma',align='center',spacing=-8)
    txt(d,(W//2,390),'For Earth, Luna, Mars and the Outer Belt — this is 2147 News Network.',BOLD(24),fill=MUTED,anchor='ma')
    strap(d,'Next','Earth Union emergency sovereignty hearing','The Mars Sovereignty Crisis continues'); ticker(d,'NEXT','EARTH UNION HEARING • 2147 NEWS NETWORK • '); return im

SCENES=[('cold',0,6),('studio',6,14),('data',14,22),('map',22,30),('archive',30,38),('quote',38,46),('market',46,54),('legal',54,60),('close',60,64)]

def frame_at(t,footage):
    for name,a,b in SCENES:
        if a<=t<b:
            if name=='cold': im=cold_open(footage)
            elif name=='studio': im=studio_layout(footage,'MARS ENTERS\nFINAL VOTING\nCYCLE','A sovereignty referendum across 42 Martian settlement zones could create the first independent off-world republic.')
            elif name=='data': im=data_wall()
            elif name=='map': im=map_wall()
            elif name=='archive': im=archive_wall(footage)
            elif name=='quote': im=quote_wall()
            elif name=='market': im=studio_layout(footage,'ENERGY MARKETS\nWATCH MARS VOTE','Helion Grid Systems warns unresolved treaty language could delay fusion-grid contracts.','+18.6%','Cargo Insurance','Financial Desk')
            elif name=='legal': im=studio_layout(footage,'AI VOTING RIGHTS\nPETITION FILED','The Synthetic Rights Tribunal receives a petition over memory-continuity residents.','3.8M','Synthetic Residents','Legal Desk')
            else: im=close_scene()
            local=t-a; fade=min(1,local/.45,(b-t)/.45)
            if fade<1: im=Image.blend(Image.new('RGBA',(W,H),(5,7,13,255)),im,ease(fade))
            return im
    return close_scene()

def transcode(src,dst):
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe(); subprocess.check_call([ff,'-y','-i',str(src),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart','-preset','medium','-crf','22',str(dst)])

def main():
    cap=cv2.VideoCapture(str(SRC)); OUT.parent.mkdir(parents=True,exist_ok=True); writer=cv2.VideoWriter(str(TMP),cv2.VideoWriter_fourcc(*'mp4v'),FPS,(W,H))
    total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1000
    for n in range(FPS*DUR):
        cap.set(cv2.CAP_PROP_POS_FRAMES,(n*2)%total); ok,fr=cap.read()
        if not ok: cap.set(cv2.CAP_PROP_POS_FRAMES,0); ok,fr=cap.read()
        footage=Image.fromarray(cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)).resize((W,H),Image.Resampling.LANCZOS).convert('RGBA')
        im=frame_at(n/FPS,footage)
        if n==FPS*8: im.convert('RGB').save(POSTER_OUT)
        writer.write(cv2.cvtColor(np.array(im.convert('RGB')),cv2.COLOR_RGB2BGR))
        if n%(FPS*8)==0: print('frame',n,'/',FPS*DUR)
    writer.release(); cap.release(); transcode(TMP,OUT); TMP.unlink(missing_ok=True); print('wrote',OUT)
if __name__=='__main__': main()
