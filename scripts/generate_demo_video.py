"""Generate a code-rendered demo video for 2147 News Network.

No AI-generated images or video are used. Frames are drawn procedurally with
Pillow/OpenCV: gradients, typography, planets, charts, panels, and tickers.
"""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 720
FPS = 24
DURATION = 42
TOTAL = FPS * DURATION
OUT = Path("outputs/demo-video/2147-demo-pilot-ui.mp4")
TMP_OUT = Path("outputs/demo-video/2147-demo-pilot-ui-mp4v-temp.mp4")
POSTER = Path("outputs/demo-video/2147-demo-poster.png")

FONT_DIRS = [
    Path("/usr/share/fonts/truetype/dejavu"),
    Path("/usr/share/fonts/truetype/liberation2"),
]

def font(name="DejaVuSans.ttf", size=40):
    for d in FONT_DIRS:
        p = d / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

F_REG = lambda s: font("DejaVuSans.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_COND = lambda s: font("DejaVuSansCondensed-Bold.ttf", s)

C = {
    "black": (3, 4, 10),
    "navy": (5, 9, 20),
    "white": (248, 250, 252),
    "muted": (148, 163, 184),
    "cyan": (0, 217, 255),
    "blue": (47, 128, 255),
    "orange": (255, 106, 42),
    "amber": (255, 176, 32),
    "green": (37, 255, 156),
    "red": (255, 59, 59),
}


def ease(x):
    x = max(0, min(1, x))
    return 1 - (1 - x) ** 3


def lerp(a, b, t):
    return int(a + (b - a) * t)


def mix(c1, c2, t):
    return tuple(lerp(a, b, t) for a, b in zip(c1, c2))


def bg(t, accent=(0, 217, 255)):
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    base = np.zeros((H, W, 3), dtype=np.uint8)
    top = np.array([7, 17, 38])
    bot = np.array([3, 4, 10])
    base[:] = (top * (1 - y) + bot * y).astype(np.uint8)[:, None, :]
    # radial glows
    for cx, cy, col, power in [
        (0.22 + 0.03 * math.sin(t), 0.16, np.array(C["blue"]), 0.22),
        (0.78, 0.22 + 0.03 * math.cos(t * 0.7), np.array(accent), 0.18),
    ]:
        d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        glow = np.clip(1 - d / 0.42, 0, 1) ** 2 * power
        base = np.clip(base + glow[..., None] * col, 0, 255).astype(np.uint8)
    im = Image.fromarray(base, "RGB").convert("RGBA")
    draw = ImageDraw.Draw(im, "RGBA")
    # perspective-ish grid
    off = int((t * 18) % 64)
    for xx in range(-64 + off, W + 64, 64):
        draw.line([(xx, int(H * 0.48)), (xx + 240, H)], fill=(255, 255, 255, 14), width=1)
    for yy in range(int(H * 0.5), H, 46):
        draw.line([(0, yy), (W, yy)], fill=(255, 255, 255, 12), width=1)
    return im


def text(draw, xy, txt, fnt, fill=C["white"], anchor=None, spacing=4, align="left"):
    draw.multiline_text(xy, txt, font=fnt, fill=fill, anchor=anchor, spacing=spacing, align=align)


def rounded(draw, box, r=24, fill=(255,255,255,20), outline=(255,255,255,38), width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def glass(im, box, r=28, fill=(255,255,255,22), outline=(255,255,255,42)):
    layer = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(layer, "RGBA")
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=1)
    # subtle top highlight
    x1,y1,x2,y2=box
    d.line([(x1+r,y1+1),(x2-r,y1+1)], fill=(255,255,255,38), width=1)
    im.alpha_composite(layer)


def logo(draw):
    rounded(draw, (44, 38, 96, 90), 16, fill=(0,217,255,45), outline=(255,255,255,45))
    text(draw, (70, 52), "47", F_BOLD(20), anchor="ma")
    text(draw, (110, 42), "2147\nNEWS NETWORK", F_BOLD(15), fill=C["white"], spacing=0)


def ticker(draw, t, msg, color=(221,251,255)):
    box = (32, H-58, W-32, H-18)
    rounded(draw, box, 22, fill=(0,0,0,100), outline=(255,255,255,28))
    full = msg + "   •   " + msg
    tw = draw.textlength(full, font=F_BOLD(15))
    x = W - ((t*90) % (tw + W))
    text(draw, (x, H-46), full, F_BOLD(15), fill=color)


def planet(draw, center, radius, kind="earth", glow=1.0):
    cx, cy = center
    if kind == "mars":
        colors = [C["orange"], (117, 35, 23), (34, 9, 9)]
        glowc = C["orange"]
    elif kind == "moon":
        colors = [(245,248,255), (130,140,154), (32,39,55)]
        glowc = (220,231,245)
    else:
        colors = [(232,251,255), (31,92,184), (7,22,52)]
        glowc = C["cyan"]
    # glow
    for i in range(10, 0, -1):
        a = int(8 * glow * i)
        draw.ellipse((cx-radius-i*8, cy-radius-i*8, cx+radius+i*8, cy+radius+i*8), outline=(*glowc, a), width=3)
    # create radial sphere
    size = radius*2
    arr = np.zeros((size, size, 4), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            dx=(x-radius)/radius; dy=(y-radius)/radius
            d=(dx*dx+dy*dy)**0.5
            if d<=1:
                light=max(0,1-((dx+0.35)**2+(dy+0.32)**2)**0.5)
                shade=max(0,1-d)
                col=np.array(colors[1])
                col=col*(0.65+0.35*shade)+np.array(colors[0])*0.45*light
                if dx>0.35 or dy>0.45: col=col*0.45+np.array(colors[2])*0.55
                arr[y,x,:3]=np.clip(col,0,255)
                arr[y,x,3]=255
    sphere=Image.fromarray(arr,"RGBA")
    draw.bitmap((cx-radius,cy-radius), sphere)


def draw_bars(draw, x, y, w, labels):
    for i,(lab,pct,col) in enumerate(labels):
        yy=y+i*50
        text(draw,(x,yy-2),lab,F_BOLD(16),fill=C["white"])
        rounded(draw,(x+150,yy,x+150+w,yy+16),8,fill=(255,255,255,25),outline=(255,255,255,20))
        rounded(draw,(x+150,yy,x+150+int(w*pct),yy+16),8,fill=(*col,210),outline=(*col,230))
        text(draw,(x+170+w,yy-7),f"{int(pct*100)}%",F_BOLD(18),fill=C["white"])


def scene_intro(t, local):
    im=bg(t)
    d=ImageDraw.Draw(im,"RGBA")
    logo(d)
    # orbit rings
    cx,cy=W//2,H//2-15
    for i,r in enumerate([150,240,330]):
        a=40+int(20*math.sin(t*2+i))
        d.ellipse((cx-r,cy-r//2,cx+r,cy+r//2), outline=(0,217,255,a), width=2)
    planet(d,(cx,cy),95,"earth")
    alpha=ease(local/0.28)
    text(d,(W//2,290),"2147\nNEWS",F_COND(94),fill=(*C["white"],int(255*alpha)),anchor="ma",spacing=-8,align="center")
    text(d,(W//2,455),"Broadcasting from tomorrow",F_BOLD(28),fill=(*C["cyan"],int(255*alpha)),anchor="ma")
    ticker(d,t,"EARTH • LUNA • MARS • OUTER BELT — TRANSMISSION VERIFIED — NEW DELHI ORBITAL BROADCAST HUB")
    return im


def scene_anchor(t, local):
    im=bg(t, C["cyan"]); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    glass(im,(40,110,W-40,H-110),34)
    # virtual map
    planet(d,(930,310),140,"earth",0.55)
    # silhouette anchor
    d.ellipse((142,250,212,320), fill=(210,245,255,160))
    d.rounded_rectangle((105,330,250,510), radius=42, fill=(255,255,255,34), outline=(255,255,255,48))
    d.rounded_rectangle((70,518,610,610), radius=34, fill=(255,255,255,30), outline=(255,255,255,45))
    # headline
    text(d,(430,180),"LIVE ANALYSIS",F_BOLD(17),fill=C["red"])
    text(d,(430,215),"Mars Enters\nFinal Voting Cycle",F_COND(62),fill=C["white"],spacing=-4)
    text(d,(430,360),"A sovereignty referendum across 42 Martian settlement zones could create the first independent off-world republic.",F_REG(24),fill=C["muted"])
    glass(im,(70,475,390,565),24,fill=(0,0,0,90),outline=(255,255,255,34))
    text(d,(95,495),"ANAYA RAO",F_BOLD(28))
    text(d,(95,533),"SENIOR ANCHOR • EARTH-ORBIT MEDIA RING",F_BOLD(12),fill=C["muted"])
    ticker(d,t,"LIVE: MARS REFERENDUM FINAL CYCLE • PROJECTED TURNOUT 91% • EARTH UNION LEGAL REVIEW BEGINS")
    return im


def scene_headlines(t, local):
    im=bg(t); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    cards=[
        (56,130,610,600,"LEAD STORY • MARS","Mars Votes\non Independence","Source: Mars Civic Council Election Board"),
        (640,130,1224,350,"MARKETS","Jiang Lau Warns of\nEnergy-Contract Instability","Source: Outer Belt Trade Registry"),
        (640,380,1224,600,"LEGAL DESK","AI Voting Rights\nPetition Filed","Source: Synthetic Rights Tribunal"),
    ]
    for i,c in enumerate(cards):
        x1,y1,x2,y2,label,head,src=c
        shift=max(0,1-ease((local-i*0.09)/0.32))*40
        glass(im,(x1,int(y1+shift),x2,int(y2+shift)),30)
        text(d,(x1+28,y1+30+shift),label,F_BOLD(14),fill=C["cyan"])
        fs=56 if i==0 else 38
        text(d,(x1+28,y1+75+shift),head,F_COND(fs),spacing=-2)
        text(d,(x1+28,y2-42+shift),src,F_BOLD(13),fill=C["muted"])
    ticker(d,t,"TOP STORIES • MARS VOTE • ENERGY CONTRACTS • LUNAR OXYGEN CREDITS • SYNTHETIC VOTING RIGHTS")
    return im


def scene_mars(t, local):
    im=bg(t,C["orange"]); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    planet(d,(250,335),150,"mars")
    for mx,my in [(275,330),(210,380),(310,410)]:
        d.ellipse((mx-7,my-7,mx+7,my+7), fill=(*C["cyan"],230))
    glass(im,(490,115,1225,620),34)
    text(d,(525,150),"MARS POLITICAL DESK",F_BOLD(15),fill=C["orange"])
    text(d,(525,188),"Mars Independence\nVote",F_COND(62),spacing=-4)
    text(d,(525,325),"Turnout and vote model across 42 recognized settlement zones.",F_REG(23),fill=C["muted"])
    stats=[("38.2M","Population"),("29.4M","Eligible Voters"),("91%","Projected Turnout")]
    for i,(v,l) in enumerate(stats):
        x=525+i*220
        rounded(d,(x,375,x+190,455),20,fill=(0,0,0,70),outline=(255,255,255,22))
        text(d,(x+18,390),v,F_BOLD(34))
        text(d,(x+18,430),l.upper(),F_BOLD(11),fill=C["muted"])
    draw_bars(d,525,490,420,[('Independence',.57,C['green']),('Union',.39,C['orange']),('Undecided',.04,C['muted'])])
    ticker(d,t,"MARS MODEL: INDEPENDENCE 57% • UNION 39% • UNDECIDED 4% • ELIGIBLE VOTERS 29.4M")
    return im


def scene_timeline(t, local):
    im=bg(t,C["orange"]); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    text(d,(60,145),"HISTORICAL TIMELINE",F_BOLD(16),fill=C["cyan"])
    text(d,(60,185),"Why This\nVote Exists",F_COND(68),spacing=-4)
    text(d,(60,340),"The referendum is the result of decades of life-support pricing disputes, cargo tariff challenges, and settlement autonomy demands.",F_REG(23),fill=C["muted"])
    glass(im,(575,115,1225,615),34)
    d.line((655,165,655,560),fill=(*C["cyan"],150),width=3)
    events=[('2136','Lunar oxygen-credit protests','Life-support pricing becomes a political issue.'),('2142','Mars challenges cargo tariffs','Earth-Mars trade authority is disputed.'),('2147','Final referendum cycle','42 settlement zones enter final voting.'),('Next','Legal and market ripples','Senate, guilds, tribunals, and markets respond.')]
    for i,(yr,ttl,desc) in enumerate(events):
        y=170+i*96
        d.ellipse((648,y-6,662,y+8),fill=(*C['cyan'],230))
        rounded(d,(595,y-20,640,y+20),18,fill=(0,0,0,90),outline=(255,255,255,25))
        text(d,(617,y-12),yr,F_BOLD(14),anchor='ma')
        rounded(d,(685,y-35,1185,y+38),20,fill=(0,0,0,55),outline=(255,255,255,20))
        text(d,(705,y-24),ttl,F_BOLD(22))
        text(d,(705,y+4),desc,F_REG(16),fill=C['muted'])
    ticker(d,t,"CAUSAL TIMELINE • 2136 OXYGEN-CREDIT PROTESTS • 2142 CARGO TARIFF DISPUTE • 2147 REFERENDUM")
    return im


def scene_quote(t, local):
    im=bg(t); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    glass(im,(95,120,1185,610),38)
    rounded(d,(135,165,390,560),32,fill=(0,217,255,24),outline=(255,255,255,34))
    d.ellipse((210,230,315,335),fill=(225,250,255,150))
    d.rounded_rectangle((175,360,350,510),radius=44,fill=(255,255,255,35),outline=(255,255,255,40))
    text(d,(445,165),"EXPERT ANALYSIS • UNIVERSITY OF VALLES MARINERIS",F_BOLD(15),fill=C['cyan'])
    text(d,(445,210),"Dr. Ilyan Sen",F_COND(58))
    text(d,(445,280),"Political Historian • Mars Colony Seven Academic District",F_BOLD(18),fill=C['muted'])
    text(d,(445,350),'“Mars is no longer an outpost.\nIt is a civilization asking for\npolitical recognition.”',F_COND(46),fill=C['white'],spacing=2)
    ticker(d,t,"EXPERT ANALYSIS • UNIVERSITY OF VALLES MARINERIS • ARCHIVE FEED VERIFIED")
    return im


def scene_finance(t, local):
    im=bg(t,C['amber']); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    glass(im,(55,115,585,620),34); glass(im,(610,115,1225,620),34)
    text(d,(90,155),"FINANCIAL DESK",F_BOLD(16),fill=C['amber'])
    text(d,(90,195),"Energy Markets\nWatch Mars Vote",F_COND(58),spacing=-3)
    text(d,(90,335),"Helion Grid Systems warns unresolved treaty language could delay fusion-grid contracts and cargo insurance pricing.",F_REG(22),fill=C['muted'])
    rounded(d,(90,455,545,585),24,fill=(0,0,0,75),outline=(255,255,255,24))
    text(d,(115,475),"JIANG LAU",F_BOLD(26)); text(d,(115,510),"CEO • HELION GRID SYSTEMS",F_BOLD(13),fill=C['muted'])
    text(d,(115,535),'“Markets cannot absorb legal uncertainty across two planets.”',F_REG(18),fill=C['white'])
    metrics=[('+18.6%','Cargo Insurance'),('14 mo.','Contract Delay Risk'),('−4.2%','Mars Infra Bonds')]
    for i,(v,l) in enumerate(metrics):
        x=645+i*185; rounded(d,(x,150,x+165,225),20,fill=(0,0,0,70),outline=(255,255,255,22)); text(d,(x+15,162),v,F_BOLD(30)); text(d,(x+15,202),l.upper(),F_BOLD(10),fill=C['muted'])
    # chart
    rounded(d,(650,270,1185,560),24,fill=(0,0,0,60),outline=(255,255,255,20))
    pts=[(675,500),(745,465),(815,480),(890,390),(970,415),(1040,335),(1120,355),(1170,300)]
    d.line(pts,fill=(*C['amber'],230),width=4)
    for p in pts: d.ellipse((p[0]-4,p[1]-4,p[0]+4,p[1]+4),fill=(*C['amber'],255))
    ticker(d,t,"HELION GRID SYSTEMS • CARGO INSURANCE +18.6% • MARS INFRASTRUCTURE BONDS −4.2% • CONTRACT RISK 14 MONTHS",(255,230,181))
    return im


def scene_legal(t, local):
    im=bg(t,(155,140,255)); d=ImageDraw.Draw(im,"RGBA"); logo(d)
    glass(im,(55,115,600,620),34); glass(im,(625,115,1225,620),34)
    text(d,(90,155),"LEGAL DESK",F_BOLD(16),fill=(210,205,255))
    text(d,(90,195),"AI Voting Rights\nPetition Filed",F_COND(56),spacing=-3)
    text(d,(90,330),"The Synthetic Rights Tribunal receives a petition over memory-continuity residents registered in Martian settlement zones.",F_REG(22),fill=C['muted'])
    rounded(d,(90,455,560,575),24,fill=(255,255,255,20),outline=(255,255,255,28))
    text(d,(115,475),"TRIBUNAL FILING",F_BOLD(13),fill=C['muted'])
    text(d,(115,505),"Referendum certification review",F_BOLD(24))
    metrics=[('42','Settlement Zones'),('3.8M','Synthetic Residents'),('Pending','Jurisdiction'),('2147-CV','Case Track')]
    for i,(v,l) in enumerate(metrics):
        x=660+(i%2)*255; y=155+(i//2)*95
        rounded(d,(x,y,x+225,y+75),20,fill=(0,0,0,65),outline=(255,255,255,22)); text(d,(x+16,y+12),v,F_BOLD(30)); text(d,(x+16,y+50),l.upper(),F_BOLD(10),fill=C['muted'])
    rounded(d,(660,370,1185,565),26,fill=(155,140,255,30),outline=(155,140,255,70))
    text(d,(690,400),"SELENE ARMITAGE",F_BOLD(25)); text(d,(690,435),"SENIOR COUNSEL • SYNTHETIC RIGHTS TRIBUNAL",F_BOLD(12),fill=C['muted'])
    text(d,(690,475),'“Memory deletion without consent is no longer a technical action. It is a civil rights violation.”',F_REG(21),fill=C['white'])
    ticker(d,t,"SYNTHETIC RIGHTS TRIBUNAL • 3.8M SYNTHETIC RESIDENTS • REFERENDUM CERTIFICATION REVIEW",(230,226,255))
    return im


def scene_close(t, local):
    im=bg(t); d=ImageDraw.Draw(im,"RGBA")
    cx,cy=W//2,H//2-20
    for r in [130,220,315]: d.ellipse((cx-r,cy-r//2,cx+r,cy+r//2),outline=(0,217,255,55),width=2)
    text(d,(W//2,250),"End\nTransmission",F_COND(92),anchor='ma',align='center',spacing=-8)
    text(d,(W//2,430),"For Earth, Luna, Mars, and the Outer Belt — this is 2147 News Network.",F_REG(27),fill=C['muted'],anchor='ma')
    text(d,(W//2,500),"BROADCAST ARCHIVE SAVED",F_BOLD(16),fill=C['cyan'],anchor='ma')
    ticker(d,t,"NEXT: EARTH UNION EMERGENCY SOVEREIGNTY HEARING • 2147 NEWS NETWORK")
    return im

SCENES=[
    (0,4,scene_intro),(4,9,scene_anchor),(9,13,scene_headlines),(13,19,scene_mars),(19,24,scene_timeline),(24,28,scene_quote),(28,33,scene_finance),(33,38,scene_legal),(38,42,scene_close)
]

def frame_at(n):
    t=n/FPS
    for start,end,fn in SCENES:
        if start<=t<end:
            local=(t-start)/(end-start)
            im=fn(t,local)
            # fade in/out
            fade=min(1, (t-start)/0.45, (end-t)/0.45)
            if fade<1:
                black=Image.new('RGBA',(W,H),(3,4,10,255))
                im=Image.blend(black,im,ease(fade))
            return im.convert('RGB')
    return scene_close(t,1).convert('RGB')


def transcode_to_browser_h264(src: Path, dst: Path):
    """Transcode OpenCV's mp4v output into browser-friendly H.264.

    GitHub/browser previews often do not play mp4v MP4 files. The
    imageio-ffmpeg package ships a static ffmpeg binary with libx264.
    """
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        print("imageio-ffmpeg unavailable; leaving mp4v output in place:", exc)
        if src != dst:
            dst.write_bytes(src.read_bytes())
        return
    cmd = [
        ffmpeg, "-y", "-i", str(src),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", "-preset", "medium", "-crf", "23",
        str(dst),
    ]
    subprocess.check_call(cmd)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    writer=cv2.VideoWriter(str(TMP_OUT), fourcc, FPS, (W,H))
    if not writer.isOpened():
        raise RuntimeError('Could not open OpenCV VideoWriter with mp4v codec')
    for n in range(TOTAL):
        im=frame_at(n)
        if n==int(FPS*2):
            im.save(POSTER)
        arr=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        writer.write(arr)
        if n % (FPS*5)==0:
            print(f'frame {n}/{TOTAL}')
    writer.release()
    transcode_to_browser_h264(TMP_OUT, OUT)
    if TMP_OUT.exists():
        TMP_OUT.unlink()
    print('wrote browser-compatible H.264', OUT)
    print('poster', POSTER)

if __name__=='__main__':
    main()
