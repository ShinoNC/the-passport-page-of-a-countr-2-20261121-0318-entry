#!/usr/bin/env python3
"""Build passport-01 spread with PIL: code-drawn typography, computed MRZ
check digits, date-consistent stamps. Output: entry.png (1024x724)."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 724
PAPER = (244, 238, 220)
PAPER2 = (238, 231, 210)
NAVY = (31, 58, 95)
NAVY_LT = (58, 88, 130)
GOLD = (138, 109, 43)
GREY = (96, 96, 90)
INK = (34, 34, 32)
BLUE = (43, 76, 140)
RED = (163, 59, 46)
TEAL = (46, 110, 106)
PURPLE = (107, 74, 140)
GREEN = (62, 107, 52)

F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
F_SI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- MRZ (ICAO 9303, weights 7-3-1) ----------
VALS = {c: i for i, c in enumerate("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ<")}
def cd(s):
    w = (7, 3, 1)
    return str(sum(VALS[c] * w[i % 3] for i, c in enumerate(s)) % 10)

line1_body = "P<KESAUNE<<MAREN<SOLVEIG"
line1 = line1_body + "<" * (44 - len(line1_body))
doc = "KS0048217"
nat = "KES"
dob = "880614"
sex = "F"
exp = "340312"
filler = "<" * 15
line2_core = doc + cd(doc) + nat + dob + cd(dob) + sex + exp + cd(exp) + filler
line2 = line2_core + cd(line2_core)
assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
print("MRZ1:", line1)
print("MRZ2:", line2)

# ---------- canvas ----------
img = Image.new("RGB", (W, H), (24, 46, 58))  # dark cover edge
paper = Image.new("RGB", (W - 16, H - 16), PAPER)
img.paste(paper, (8, 8))
d = ImageDraw.Draw(img, "RGBA")
OX, OY = 8, 8  # paper origin

def ls_draw(draw, xy, text, fnt, fill, spacing=0):
    """Draw text with letter spacing; returns width."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x

def center_ls(draw, cx, y, text, fnt, fill, spacing=0):
    w = sum(draw.textlength(c, font=fnt) + spacing for c in text) - spacing
    ls_draw(draw, (cx - w / 2, y), text, fnt, fill, spacing)
    return w

def field(draw, x, y, w, label, value, vsize=15):
    draw.text((x, y), label, font=font(F_R, 9), fill=GREY)
    draw.text((x, y + 11), value, font=font(F_B, vsize), fill=INK)
    draw.line([(x, y + 30), (x + w, y + 30)], fill=(190, 182, 160), width=1)

# ---------- guilloche: faint concentric arcs ----------
for cx, cy, r0 in ((120, 640, 60), (920, 90, 60), (512, 362, 200)):
    for r in range(r0, r0 + 220, 14):
        d.ellipse([OX + cx - r, OY + cy - r, OX + cx + r, OY + cy + r],
                  outline=(31, 58, 95, 14), width=1)

# centre gutter + page borders
d.line([(OX + 504, OY + 10), (OX + 504, OY + 694)], fill=(120, 110, 88), width=2)
d.rectangle([OX + 4, OY + 4, OX + 1003, OY + 699], outline=NAVY, width=2)

# ---------- emblem: circle + three peaks ----------
def emblem(cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4], outline=color, width=1)
    pts = [(cx - r + 7, cy + 8), (cx - 9, cy - 12), (cx - 1, cy + 2),
           (cx + 6, cy - 16), (cx + 13, cy + 2), (cx + r - 7, cy + 8)]
    d.line(pts, fill=color, width=2)
    d.line([(cx - r + 7, cy + 12), (cx + r - 7, cy + 12)], fill=color, width=2)

# ================= LEFT PAGE (x 12..504) =================
LX = OX + 14
emblem(LX + 30, OY + 44, 26, NAVY)
d.text((LX + 68, OY + 22), "THE HIGH REPUBLIC OF KESTRA", font=font(F_B, 24), fill=NAVY)
center_ls(d, LX + 68 + 190, OY + 52, "RÉPUBLIQUE DE KESTRA", font(F_R, 10), GOLD, spacing=3)
d.line([(LX, OY + 78), (LX + 476, OY + 78)], fill=NAVY, width=2)
center_ls(d, LX + 238, OY + 90, "PASSPORT  /  PASSEPORT", font(F_B, 13), NAVY, spacing=2)

# portrait
portrait = Image.open("media-generation-kestra-portrait-0-99686f80-ecf7-4b93-831b-3eb3e85bcd68.png").convert("RGB")
pw, ph = portrait.size
# head-and-shoulders crop: centre horizontally, top 2% to 62%
crop = portrait.crop((int(pw * 0.16), int(ph * 0.01), int(pw * 0.84), int(ph * 0.60)))
crop = crop.resize((148, 186), Image.LANCZOS)
img.paste(crop, (LX + 22, OY + 122))
d.rectangle([LX + 22, OY + 122, LX + 170, OY + 308], outline=NAVY, width=2)
# round seal overlapping photo corner
sx, sy, sr = LX + 140, OY + 278, 22
seal = Image.new("RGBA", (sr * 2 + 8, sr * 2 + 8), (0, 0, 0, 0))
sd = ImageDraw.Draw(seal)
sd.ellipse([4, 4, sr * 2 + 4, sr * 2 + 4], outline=BLUE + (230,), width=2)
sd.ellipse([10, 10, sr * 2 - 2, sr * 2 - 2], outline=BLUE + (230,), width=1)
sd.text((sr + 4 - 26, sr - 14), "PASSGATE", font=font(F_B, 9), fill=BLUE + (230,))
sd.text((sr + 4 - 24, sr - 1), "12 MAR 2024", font=font(F_B, 8), fill=BLUE + (230,))
seal = seal.rotate(12, expand=True, resample=Image.BICUBIC)
img.paste(seal, (sx - sr - 4, sy - sr - 4), seal)

# signature under photo
d.text((LX + 22, OY + 316), "Maren Solveig Aune", font=font(F_SI, 17), fill=INK)
d.line([(LX + 22, OY + 338), (LX + 170, OY + 338)], fill=INK, width=1)
d.text((LX + 22, OY + 342), "HOLDER'S SIGNATURE", font=font(F_R, 8), fill=GREY)

# fields right of photo
fx, fw = LX + 190, 286
rows = [
    ("SURNAME", "AUNE"),
    ("GIVEN NAMES", "MAREN SOLVEIG"),
    ("NATIONALITY", "KESTRAN"),
    ("DATE OF BIRTH", "14 JUN 1988"),
    ("SEX", "F"),
    ("PLACE OF BIRTH", "PASSGATE"),
]
y = OY + 122
for label, value in rows:
    field(d, fx, y, fw, label, value)
    y += 33

# lower fields, two columns
y0 = OY + 356
field(d, LX + 22, y0, 210, "DATE OF ISSUE", "12 MAR 2024")
field(d, LX + 266, y0, 210, "OCCUPATION", "MOUNTAIN GUIDE")
field(d, LX + 22, y0 + 40, 210, "DATE OF EXPIRY", "12 MAR 2034")
field(d, LX + 266, y0 + 40, 210, "HEIGHT", "172 cm")
field(d, LX + 22, y0 + 80, 210, "PASSPORT NO.", "KS 0048217")
field(d, LX + 266, y0 + 80, 210, "EYES", "BROWN")
field(d, LX + 22, y0 + 120, 454, "AUTHORITY", "PASSGATE PASS OFFICE")

# condition box
bx, by, bw, bh = LX + 22, OY + 512, 454, 78
d.rectangle([bx, by, bx + bw, by + bh], outline=TEAL, width=2)
d.text((bx + 10, by + 7), "CONDITION OF ISSUE", font=font(F_B, 10), fill=TEAL)
cond = ("This passport is valid only above 2,000 metres. The holder must report "
        "to a pass office within one day of every crossing, and may not travel "
        "by motor vehicle above the snow line.")
# manual wrap
words, lines, cur = cond.split(), [], ""
for w_ in words:
    t = (cur + " " + w_).strip()
    if d.textlength(t, font=font(F_R, 11)) <= bw - 20:
        cur = t
    else:
        lines.append(cur)
        cur = w_
lines.append(cur)
yy = by + 24
for ln in lines:
    d.text((bx + 10, yy), ln, font=font(F_R, 11), fill=INK)
    yy += 15

# MRZ
d.rectangle([LX + 22, OY + 606, LX + 476, OY + 652], fill=PAPER2)
d.text((LX + 30, OY + 610), line1, font=font(F_M, 13), fill=INK)
d.text((LX + 30, OY + 630), line2, font=font(F_M, 13), fill=INK)
d.text((LX + 22, OY + 668), "2", font=font(F_R, 10), fill=GREY)
d.text((LX + 22, OY + 682), "This passport remains the property of the High Republic of Kestra.",
       font=font(F_SI, 9), fill=GREY)

# ================= RIGHT PAGE (x 524..1008) =================
RX = OX + 516
d.text((RX + 12, OY + 22), "VISAS / VISAS — ENTRIES & DEPARTURES", font=font(F_B, 15), fill=NAVY)
d.line([(RX + 12, OY + 48), (RX + 472, OY + 48)], fill=NAVY, width=2)
d.text((RX + 452, OY + 22), "3", font=font(F_R, 10), fill=GREY)

# visitor visa box
vx, vy, vw, vh = RX + 12, OY + 62, 460, 62
d.rectangle([vx, vy, vx + vw, vy + vh], outline=BLUE, width=2)
d.text((vx + 12, vy + 7), "FREE CITY OF ORRE", font=font(F_B, 13), fill=BLUE)
d.text((vx + 12, vy + 26), "VISITOR VISA — SINGLE ENTRY · 30 DAYS", font=font(F_B, 11), fill=INK)
d.text((vx + 12, vy + 44), "ISSUED AT PASSGATE — 02 SEP 2025 · VISA NO. OR-22140",
       font=font(F_R, 10), fill=GREY)

def stamp(x, y, w, h, color, lines, rot):
    layer = Image.new("RGBA", (w + 30, h + 30), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.rounded_rectangle([15, 15, 15 + w, 15 + h], radius=8, outline=color + (235,), width=2)
    yy = 15 + 8
    for txt, fnt, fill in lines:
        tw = sd.textlength(txt, font=fnt)
        sd.text((15 + (w - tw) / 2, yy), txt, font=fnt, fill=fill + (235,))
        yy += fnt.size + 3
    layer = layer.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (x - 15, y - 15), layer)

def stamp_lines(country, kind, place, date):
    return [
        (country, font(F_B, 13), None),
        (kind, font(F_R, 10), None),
        (place, font(F_R, 10), None),
        (date, font(F_B, 12), None),
    ]

# stamp grid: 2 cols x 3 rows
sw, sh = 222, 74
grid = [
    ("VALDORIA", "ARRIVAL", "KESTREL PASS · 2,847 M", "18 APR 2024", BLUE, -1.5),
    ("VALDORIA", "DEPARTURE", "KESTREL PASS · 2,847 M", "02 MAY 2024", BLUE, 1.2),
    ("ORRE", "ARRIVAL", "WOLF GATE · 2,310 M", "09 SEP 2025", RED, 1.5),
    ("ORRE", "DEPARTURE", "WOLF GATE · 2,310 M", "23 SEP 2025", RED, -1.0),
    ("MERK", "ARRIVAL", "THE OLD ROAD · 1,985 M", "27 JAN 2026", TEAL, -1.2),
    ("MERK", "DEPARTURE", "THE OLD ROAD · 1,985 M", "05 FEB 2026", TEAL, 1.5),
]
gy = OY + 140
for i, (c, k, p, dt, col, rot) in enumerate(grid):
    cx = RX + 12 + (i % 2) * (sw + 16)
    cy = gy + (i // 2) * (sh + 14)
    stamp(cx, cy, sw, sh, col,
          [(t, f, col) for (t, f, _) in stamp_lines(c, k, p, dt)], rot)

# pass permit stamp (purple, diagonal)
py = gy + 3 * (sh + 14) + 8
stamp(RX + 30, py, 300, 66, PURPLE,
      [("PASS PERMIT", font(F_B, 15), PURPLE),
       ("KESTREL PASS — ON FOOT ONLY", font(F_B, 11), PURPLE),
       ("VALID 48 HOURS FROM STAMP · 18 APR 2024", font(F_R, 10), PURPLE)], -3)
# fee stamp (green)
stamp(RX + 356, py + 6, 116, 56, GREEN,
      [("FEE PAID", font(F_B, 12), GREEN),
       ("12 KESTRELS", font(F_B, 10), GREEN),
       ("12 MAR 2024", font(F_R, 9), GREEN)], 2)

# pass heights table
ty = py + 96
d.text((RX + 12, ty), "PASS HEIGHTS — THE THREE PASSES OF KESTRA", font=font(F_B, 10), fill=NAVY)
d.line([(RX + 12, ty + 18), (RX + 472, ty + 18)], fill=NAVY, width=1)
passes = [("KESTREL PASS", "2,847 m"), ("WOLF GATE", "2,310 m"), ("THE OLD ROAD", "1,985 m")]
yy = ty + 26
for name, ht in passes:
    d.text((RX + 12, yy), name, font=font(F_R, 11), fill=INK)
    tw = d.textlength(ht, font=font(F_B, 11))
    d.text((RX + 472 - tw, yy), ht, font=font(F_B, 11), fill=INK)
    dots_x = RX + 12 + d.textlength(name, font=font(F_R, 11)) + 8
    dots_end = RX + 472 - tw - 8
    x = dots_x
    while x < dots_end:
        d.point((x, yy + 8), fill=GREY)
        x += 4
    yy += 20
d.text((RX + 12, OY + 668), "This page remains the property of the Pass Office.",
       font=font(F_SI, 9), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
import os
print("bytes:", os.path.getsize("entry.png"))
