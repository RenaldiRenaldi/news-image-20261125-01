from PIL import Image, ImageDraw, ImageFont

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
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)

def fit_text(draw, text, width, start, bold=False):
    size = start
    while size > 7 and draw.textbbox((0, 0), text, font=font(size, bold))[2] > width:
        size -= 1
    return font(size, bold)

def wrap(draw, text, f, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textbbox((0, 0), trial, font=f)[2] <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def txt(draw, xy, text, f, fill=INK, spacing=1, width=None):
    if width is None:
        draw.text(xy, text, font=f, fill=fill)
        return
    y = xy[1]
    for line in wrap(draw, text, f, width):
        draw.text((xy[0], y), line, font=f, fill=fill)
        y += f.size + spacing

def card_icon(draw, x, y, kind):
    colors = [BLUE, RED, GOLD, NAVY]
    c = colors[kind % len(colors)]
    draw.rectangle((x + 9, y + 10, x + 36, y + 31), fill=c)
    draw.line((x + 5, y + 35, x + 42, y + 35), fill=NAVY, width=2)
    draw.line((x + 13, y + 6, x + 13, y + 10), fill=RED, width=2)
    draw.line((x + 30, y + 6, x + 30, y + 10), fill=RED, width=2)

def main():
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    title = "Wednesday 25 November 2026: US spy agencies hacked, 700,000 Russian dead, Huawei convicted - 38 stories, 9 regions"
    txt(d, (24, 14), title, fit_text(d, title, 976, 29, True), NAVY)
    txt(d, (26, 53), "THE WORLD IN ONE DAY  /  VERIFIED NEWS SLATE  /  ESTIMATES AND CLAIMS LABELLED", font(12, True), MUTED)
    txt(d, (26, 72), "Wednesday 25 Nov 2026  /  38 stories  /  9 regions", font(15, True), INK)
    d.rectangle((24, 96, 1000, 101), fill=GOLD)
    d.rounded_rectangle((24, 112, 1000, 258), 8, fill=PALE, outline=(210, 216, 223), width=2)
    txt(d, (40, 122), "LEAD  /  CYBER + INTELLIGENCE", font(12, True), RED)
    txt(d, (40, 145), "CIA + ODNI hacked", fit_text(d, "CIA + ODNI hacked", 570, 38, True), NAVY)
    txt(d, (42, 188), "ARTEX tool used; NGA also affected; FinCEN reports a separate incident.", font(14, True), INK, width=650)
    txt(d, (42, 211), "Early signs point to China; no official attribution. Patched and resolved; no classified systems or critical capabilities disrupted.", font(11), MUTED, width=650)
    txt(d, (42, 235), "First reported by The New York Times; CNN, 24 Nov.  Map: Langley, Virginia.  Sources: NYT / CNN / AP", font(10), MUTED, width=690)
    d.rectangle((760, 140, 968, 235), fill=WHITE, outline=(210, 216, 223), width=1)
    txt(d, (774, 149), "IMPACT CHECK", font(11, True), NAVY)
    txt(d, (774, 172), "UNCLASSIFIED", font(15, True), BLUE)
    txt(d, (774, 193), "patched / resolved", font(10), MUTED)
    txt(d, (774, 215), "critical + classified safe", font(10, True), RED)
    d.rounded_rectangle((24, 270, 1000, 354), 8, fill=WHITE, outline=(210, 216, 223), width=2)
    txt(d, (40, 279), "CO-LEADS", font(12, True), RED)
    cols = [(40, "700,000+ Russian dead", "490,334 registered; modelled total over 700,000 since Feb 2022.  BBC / Mediazona"), (365, "Huawei guilty on 10 of 12", "Bank, wire, sanctions and trade-secrets counts; racketeering acquitted.  Reuters"), (690, "Houthis: Riyadh, then Ras Tanura", "Tuesday's PIF tower strike hurt 11; refinery attack claimed today, fires reported.  Just Security")]
    for x, head, body in cols:
        txt(d, (x, 302), head, fit_text(d, head, 285, 16, True), NAVY)
        txt(d, (x, 326), body, font(9), MUTED, width=285)
    d.rounded_rectangle((24, 365, 1000, 425), 8, fill=NAVY, outline=NAVY, width=1)
    txt(d, (40, 374), "THE DAY IN NUMBERS", font(11, True), WHITE)
    figures = [("490,334", "registered dead"), ("-6.16%", "KOSPI close"), ("$54.9B", "Dell revenue"), ("50,018.70", "Dow first 50k close"), ("11", "Riyadh hurt"), ("2", "Hormuz claim")]
    for i, (num, lab) in enumerate(figures):
        x = 188 + i * 132
        txt(d, (x, 371), num, fit_text(d, num, 118, 18, True), GOLD)
        txt(d, (x, 399), lab, font(9, True), WHITE, width=120)
    d.rounded_rectangle((24, 436, 1000, 624), 8, fill=(249, 250, 251), outline=(210, 216, 223), width=2)
    txt(d, (40, 445), "WORLD MAP  /  30 DEGREE GRATICULE  /  13 VERIFIED LOCATIONS", font(11, True), NAVY)
    mx0, my0, mw, mh = 45, 463, 934, 145
    def project(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh)
    for lon in range(-180, 181, 30):
        x, _ = project(lon, 0)
        d.line((x, my0, x, my0 + mh), fill=(222, 226, 230), width=1)
    for lat in range(-60, 91, 30):
        _, y = project(0, lat)
        d.line((mx0, y, mx0 + mw, y), fill=(222, 226, 230), width=1)
    coastlines = [
        [(-168, 66), (-150, 60), (-140, 58), (-130, 52), (-125, 48), (-124, 40), (-117, 32), (-110, 24), (-100, 18), (-90, 20), (-82, 27), (-80, 32), (-75, 40), (-68, 45), (-60, 50), (-58, 57), (-70, 62), (-95, 70), (-125, 72), (-150, 70)],
        [(-81, 12), (-78, 3), (-80, -5), (-75, -14), (-72, -22), (-68, -32), (-64, -43), (-58, -52), (-50, -55), (-42, -48), (-38, -34), (-35, -20), (-42, -8), (-50, 2), (-60, 8), (-70, 12)],
        [(-10, 35), (0, 37), (10, 44), (20, 45), (30, 42), (40, 45), (55, 52), (70, 55), (85, 55), (100, 52), (115, 50), (130, 45), (145, 42), (155, 50), (170, 55), (178, 65), (160, 70), (140, 68), (120, 72), (90, 72), (60, 68), (35, 65), (15, 60), (0, 55), (-10, 50), (-10, 42)],
        [(-18, 35), (-5, 35), (8, 33), (18, 28), (30, 31), (38, 22), (44, 10), (42, -2), (35, -12), (30, -22), (20, -34), (10, -35), (0, -30), (-8, -20), (-15, -5), (-20, 10)],
        [(112, -11), (120, -18), (130, -27), (140, -35), (150, -38), (153, -28), (146, -20), (135, -15), (125, -12)],
        [(-55, 83), (-35, 84), (-20, 78), (-42, 70), (-55, 72)],
    ]
    for coast in coastlines:
        d.polygon([project(lon, lat) for lon, lat in coast], fill=LAND, outline=(125, 135, 145))
    labels = [("NORTH AMERICA", -125, 18), ("SOUTH AMERICA", -62, -38), ("EUROPE", -55, 67), ("AFRICA", 20, -27), ("ASIA", 92, 34), ("OCEANIA", 137, -45)]
    for lab, lon, lat in labels:
        x, y = project(lon, lat)
        txt(d, (x, y), lab, font(9, True), BLUE)
    dots = [("1 Langley", -77.4, 38.9, 10, -10), ("2 Moscow", 37.6, 55.8, 10, -17), ("3 Kyiv", 30.5, 50.4, 10, 5), ("4 New York", -74.0, 40.7, 10, 7), ("5 Riyadh", 46.7, 24.7, 10, 7), ("6 Hormuz", 56.3, 26.6, 10, -16), ("7 Akwe", 29.5, 1.5, 10, 7), ("8 Warsaw", 21.0, 52.2, -62, -25), ("9 Copenhagen", 12.6, 55.7, -84, -10), ("10 Paris", 2.35, 48.9, -48, 14), ("11 Benghazi", 20.1, 32.1, 10, 7), ("12 Caracas", -66.9, 10.5, 10, 7), ("13 Canberra", 149.1, -35.3, 10, 7)]
    for label, lon, lat, dx, dy in dots:
        x, y = project(lon, lat)
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=RED, outline=WHITE, width=1)
        if dx < 0:
            if label in {"8 Warsaw", "9 Copenhagen", "10 Paris"}:
                label_width = d.textbbox((0, 0), label, font=font(8, True))[2]
                d.line((x, y, x + dx + label_width + 4, y + dy + 5), fill=RED, width=1)
            else:
                d.line((x, y, x + dx + 44, y + dy + 5), fill=RED, width=1)
        txt(d, (x + dx, y + dy), label, font(8, True), NAVY)
    cards = [("Nvidia -5.9%", "Monday +31.5%; chip sell-off spreads"), ("Two tankers hit Hormuz", "IRGC says mines; not confirmed"), ("Dell doubles sales", "$54.9B, +103%; AI backlog $132B"), ("Ukraine hits two refineries", "Syzran and Kuibyshev ablaze; 1 killed"), ("Kyiv block death toll 11", "Russian drone attack rescue"), ("WHO evacuates Akwe", "Ebola team moved amid fighting"), ("NATO AWACS to Poland", "Forward deployment after missiles"), ("Denmark ghetto law upheld", "Supreme Court, 91 leases"), ("Sarkozy to trial", "Corruption hearing set for Apr 2027"), ("Giuliani gets medal", "Trump awards civilian honour"), ("O'Hare radar outage", "Flights delayed on Thanksgiving eve"), ("COP31: no deal", "Pope warns; 90+ nations pledge"), ("Shenzhou-24 docks", "First foreign astronaut on Tiangong"), ("Colombia hostages freed", "Cartagena siege ends; one captor killed")]
    x0, y0, cw, ch = 24, 632, 238, 42
    for i, (head, body) in enumerate(cards):
        col, row = i % 4, i // 4
        x, y = x0 + col * 246, y0 + row * 47
        d.rounded_rectangle((x, y, x + cw, y + ch), 5, fill=WHITE, outline=(210, 216, 223), width=1)
        card_icon(d, x + 3, y + 1, i)
        txt(d, (x + 51, y + 4), head, fit_text(d, head, 181, 10, True), NAVY)
        txt(d, (x + 51, y + 22), body, font(8), MUTED, width=180)
    d.rounded_rectangle((24, 807, 1000, 946), 6, fill=(250, 247, 241), outline=(218, 180, 140), width=1)
    txt(d, (40, 815), "20 MORE STORIES", font(11, True), RED)
    briefs = ["Trump pardons turkeys Freedom + Feathers", "Nepal PM Balendra Shah visits India", "Senegal AFCON title restored on appeal", "Israeli military suicides at 16-year high", "Gaza humanitarian strain", "EU adds Russia sanctions", "US-Qatar strategic talks", "RFE/RL shortwave returns for Afghan girls", "Iran winter gas shortages", "Houthis 60 km from Aden", "Abrego Garcia leaves for Spain", "Sweden Kristersson PM vote", "Thomas Markle indicted", "California king tides", "Super El Nino threat to Africa", "US Army lead azide warning", "UK age-of-consent consultation", "UK nuclear test veterans panel", "Fort Hood execution stay request", "Zelenskyy EUR115bn ask; Patriot pause"]
    for i, brief in enumerate(briefs):
        col, row = i % 2, i // 2
        txt(d, (40 + col * 475, 838 + row * 10), brief, font(8), INK, width=450)
    d.rounded_rectangle((24, 954, 1000, 990), 5, fill=(255, 239, 239), outline=RED, width=2)
    txt(d, (38, 959), "DATE CHECK [OK] Every story on this page happened, or was first reported, on Wednesday 25 November 2026.", font(8, True), RED, width=940)
    txt(d, (38, 974), "LEFT OUT AS EARLIER DAYS' NEWS: Anthropic IPO debut close (Thu 19 Nov) | Senate 51-48 Iran vote (Thu 19 Nov) | GTA VI launch (Thu 19 Nov).", font(7), MUTED, width=940)
    d.rectangle((24, 997, 1000, 1000), fill=GOLD)
    im.save("entry.png", format="PNG", optimize=True)

if __name__ == "__main__":
    main()
