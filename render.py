from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
NAVY = (17, 38, 70)
BLUE = (39, 104, 166)
GOLD = (208, 155, 44)
RED = (178, 55, 54)
INK = (36, 43, 52)
MUTED = (99, 111, 124)
PALE = (240, 243, 246)
LAND = (224, 228, 232)
WHITE = (255, 255, 255)

def font(size, bold=False):
    name = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(name, size)

def fit_text(draw, text, max_width, start, bold=False):
    s = start
    while s > 8 and draw.textbbox((0,0), text, font=font(s,bold))[2] > max_width:
        s -= 1
    return font(s,bold)

def wrap(draw, text, f, width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=f)[2] <= width: line = test
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def txt(draw, xy, text, f, fill=INK, spacing=2, width=None):
    if width:
        y = xy[1]
        for line in wrap(draw,text,f,width):
            draw.text((xy[0],y),line,font=f,fill=fill)
            y += f.size + spacing
        return y
    draw.text(xy,text,font=f,fill=fill)

def card_icon(d, x, y, kind):
    # Each card gets a small, distinct two-to-four shape illustration.
    if kind == 0: # chip
        d.rounded_rectangle((x+10,y+7,x+42,y+37),5,fill=BLUE,outline=NAVY,width=2)
        for i in range(4):
            d.line((x+5+i*10,y+2,x+5+i*10,y+7),fill=RED,width=2)
            d.line((x+5+i*10,y+37,x+5+i*10,y+42),fill=RED,width=2)
        d.rectangle((x+20,y+16,x+31,y+27),fill=GOLD)
    elif kind == 1: # bar chart
        d.line((x+8,y+40,x+8,y+5),fill=NAVY,width=3); d.line((x+8,y+40,x+48,y+40),fill=NAVY,width=3)
        for i,h in enumerate((15,27,34)): d.rectangle((x+14+i*11,y+40-h,x+22+i*11,y+40),fill=(BLUE if i<2 else RED))
    elif kind == 2: # drone/tower
        d.rectangle((x+24,y+8,x+39,y+38),fill=RED); d.line((x+31,y+38,x+31,y+44),fill=NAVY,width=2)
        d.ellipse((x+5,y+16,x+20,y+25),outline=BLUE,width=3); d.line((x+20,y+20,x+29,y+20),fill=BLUE,width=2)
    elif kind == 3: # ship
        d.polygon([(x+5,y+27),(x+46,y+27),(x+37,y+38),(x+14,y+38)],fill=BLUE)
        d.line((x+25,y+27,x+25,y+8),fill=NAVY,width=2); d.polygon([(x+26,y+9),(x+41,y+17),(x+26,y+20)],fill=GOLD)
    elif kind == 4: # shield
        d.polygon([(x+27,y+5),(x+45,y+12),(x+42,y+29),(x+27,y+41),(x+12,y+29),(x+9,y+12)],fill=BLUE)
        d.line((x+19,y+23,x+25,y+29),fill=WHITE,width=3); d.line((x+25,y+29,x+36,y+16),fill=WHITE,width=3)
    elif kind == 5: # virus
        d.ellipse((x+13,y+10,x+41,y+38),fill=RED)
        for a in range(0,360,60):
            xx,yy=x+27+20*math.cos(math.radians(a)),y+24+20*math.sin(math.radians(a)); d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=GOLD)
    elif kind == 6: # ballot
        d.rectangle((x+10,y+8,x+44,y+39),outline=NAVY,width=3,fill=WHITE); d.line((x+17,y+16,x+37,y+16),fill=BLUE,width=2); d.line((x+17,y+24,x+37,y+24),fill=BLUE,width=2); d.line((x+17,y+32,x+30,y+32),fill=RED,width=2)
    elif kind == 7: # plane/radar
        d.arc((x+5,y+7,x+48,y+49),210,330,fill=BLUE,width=2); d.line((x+27,y+29,x+45,y+11),fill=RED,width=3); d.ellipse((x+23,y+25,x+31,y+33),fill=GOLD)
    elif kind == 8: # flame/gas
        d.polygon([(x+26,y+42),(x+12,y+29),(x+18,y+10),(x+28,y+20),(x+37,y+5),(x+44,y+28)],fill=RED)
        d.ellipse((x+23,y+26,x+34,y+39),fill=GOLD)
    elif kind == 9: # sports
        d.ellipse((x+10,y+8,x+40,y+38),fill=GOLD,outline=NAVY,width=2); d.arc((x+15,y+13,x+35,y+33),30,210,fill=BLUE,width=2); d.arc((x+15,y+13,x+35,y+33),210,350,fill=RED,width=2)
    elif kind == 10: # coral
        d.line((x+27,y+40,x+27,y+16),fill=RED,width=4); d.line((x+27,y+27,x+15,y+16),fill=RED,width=3); d.line((x+27,y+30,x+39,y+18),fill=RED,width=3); d.ellipse((x+8,y+36,x+46,y+43),fill=BLUE)
    elif kind == 11: # eye/telescope
        d.ellipse((x+8,y+14,x+45,y+36),outline=BLUE,width=3); d.ellipse((x+23,y+20,x+31,y+28),fill=RED); d.line((x+27,y+36,x+27,y+44),fill=NAVY,width=3)
    else: # courthouse
        d.polygon([(x+8,y+15),(x+27,y+5),(x+46,y+15)],fill=GOLD); d.rectangle((x+11,y+17,x+43,y+38),outline=NAVY,width=2)
        for xx in (x+16,x+26,x+36): d.line((xx,y+19,xx,y+36),fill=BLUE,width=2)

def main():
    im=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(im)
    # Masthead
    title="Wednesday 25 November 2026: US spy agencies hacked, 700,000 Russian dead, Huawei convicted — 38 stories, 9 regions"
    tf=fit_text(d,title,970,31,True); txt(d,(26,18),title,tf,NAVY)
    txt(d,(28,62),"THE WORLD IN ONE DAY  /  VERIFIED NEWS SLATE  /  ESTIMATES AND CLAIMS LABELLED",font(13,True),MUTED)
    txt(d,(28,84),"Wednesday 25 Nov 2026  •  38 stories  •  9 regions  •  18 fields",font(16,True),INK)
    d.rectangle((26,113,998,119),fill=GOLD)
    # Lead panel
    d.rounded_rectangle((26,132,998,355),8,fill=PALE,outline=(210,216,223),width=2)
    txt(d,(44,145),"LEAD  /  CYBER + INTELLIGENCE",font(14,True),RED)
    lf=fit_text(d,"CIA + ODNI hacked",550,42,True); txt(d,(44,169),"CIA + ODNI hacked",lf,NAVY)
    txt(d,(46,226),"US spy agencies' unclassified intel system was breached.",font(18,True),INK)
    txt(d,(46,255),"Officials say no classified information or critical capabilities were affected.",font(15),MUTED,width=610)
    txt(d,(46,285),"First reported by The New York Times; CNN, 24 Nov.  Map: Langley, Virginia.",font(14),MUTED,width=610)
    # data chart
    d.line((705,300,950,300),fill=NAVY,width=2)
    for i,(lab,val,col) in enumerate([("OPEN-SOURCE",78,BLUE),("CLASSIFIED",4,RED),("CAPABILITIES",18,GOLD)]):
        x=715+i*78; d.rectangle((x,300-val,x+38,300),fill=col); txt(d,(x-5,306),lab,font(8,True),MUTED)
    txt(d,(706,156),"IMPACT CHECK",font(12,True),NAVY); txt(d,(706,176),"unclassified hit",font(17,True),BLUE); txt(d,(706,202),"classified systems safe",font(14,True),RED)
    # co-leads
    d.rounded_rectangle((26,368,998,487),8,fill=WHITE,outline=(210,216,223),width=2)
    txt(d,(44,380),"CO-LEADS",font(14,True),RED)
    cols=[(44,"700,000+ killed, analysis finds","Modelled estimate: 490k registered; >700k estimated since Feb 2022."),(366,"Huawei guilty on 10 of 12 counts","New York jury: bank fraud and trade-secrets theft, 24 Nov."),(688,"Houthis hit Riyadh tower","Drone strike on PIF HQ; at least 11 hurt, second strike in <1 week.")]
    for x,head,body in cols:
        hf=fit_text(d,head,270,20,True); txt(d,(x,410),head,hf,NAVY); txt(d,(x,438),body,font(12),MUTED,width=270)
    # map
    d.rounded_rectangle((26,500,998,715),8,fill=(249,250,251),outline=(210,216,223),width=2)
    txt(d,(44,511),"38 STORIES / 9 REGIONS",font(13,True),NAVY)
    # graticule
    for gy in range(545,690,36): d.line((55,gy,970,gy),fill=(215,220,225),width=1)
    for gx in range(100,951,85): d.line((gx,535,gx,695),fill=(225,229,233),width=1)
    # coarse but geographically placed land silhouettes
    land=[[(70,570),(130,548),(205,550),(250,580),(230,610),(180,615),(145,640),(115,625)],[(285,555),(345,545),(395,560),(425,585),(410,625),(370,650),(335,625),(300,600)],[(455,548),(505,545),(550,560),(590,585),(620,600),(650,590),(700,610),(745,600),(790,625),(850,615),(900,630),(940,660),(900,680),(820,675),(755,665),(700,680),(630,660),(580,645),(525,625),(480,595)],[(760,545),(800,535),(835,555),(820,580),(785,590)],[(855,650),(920,655),(950,680),(900,692),(850,680)]]
    for poly in land: d.polygon(poly,fill=LAND,outline=(125,135,145))
    dots=[(155,570,"1 Langley"),(333,570,"2 Moscow/Kyiv"),(210,602,"3 New York"),(648,618,"4 Riyadh"),(515,552,"5 Gulf"),(590,610,"6 Hormuz"),(515,645,"7 Akwe"),(430,565,"8 Warsaw"),(465,555,"9 Copenhagen"),(450,580,"10 Paris"),(710,650,"11 Benghazi"),(240,625,"12 Caracas"),(870,672,"13 Canberra")]
    for i,(x,y,label) in enumerate(dots):
        d.ellipse((x-7,y-7,x+7,y+7),fill=RED,outline=WHITE,width=2); d.text((x+10,y-8),label,font=font(11,True),fill=NAVY)
    # cards
    cards=[("Nvidia slides 7.5%","$152.76 after Monday's surge"),("Sparta II strike confirmed","Ukraine says cargo ship carried weapons"),("Kyiv block death toll 11","Russian drone attack rescue"),("Iran tanker report","IRGC claim; US denies; unverified"),("WHO evacuates Akwe","Ebola team moved amid fighting"),("NATO AWACS to Poland","Forward deployment after missiles"),("Denmark ghetto law upheld","91 leases case, unanimous court"),("Sarkozy to trial","Corruption hearing set for Apr 2027"),("Giuliani gets medal","Trump awards civilian honour"),("O'Hare radar outage","Flights delayed on Thanksgiving eve"),("Dell lifts forecast","Record AI server quarter"),("England level T20 series","Beat Australia by 8 wickets"),("COP31 aftermath","No deal; 90+ nations sign pledge"),("Venezuela debt report","Public debt reported at $237.5B")]
    x0,y0=26,724; cw,ch=238,66
    for i,(head,body) in enumerate(cards):
        col=i%4; row=i//4; x=x0+col*246; y=y0+row*70
        d.rounded_rectangle((x,y,x+cw,y+ch),6,fill=WHITE,outline=(210,216,223),width=2)
        card_icon(d,x+5,y+12,i)
        hf=fit_text(d,head,177,13,True); txt(d,(x+58,y+7),head,hf,NAVY); txt(d,(x+58,y+29),body,font(9),MUTED,width=170)
    # footer
    d.rectangle((26,1000,998,1003),fill=GOLD)
    txt(d,(28,1007),"38 STORIES  •  9 REGIONS  •  18 FIELDS  |  Estimates and unverified claims are marked",font(10,True),MUTED)
    im.save("entry.png",format="PNG",optimize=True)

if __name__ == "__main__": main()
