#!/usr/bin/env python3
"""Render an invented passport spread for the Republic of Kaldrin.

Deterministic, stdlib + Pillow only, no network. Writes entry.png
(1024x640) next to this file. Run: python3 draw.py
"""
import hashlib
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 640
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

CREAM = (244, 238, 222)
CREAM2 = (238, 231, 210)
TEAL = (18, 74, 78)
TEAL_D = (10, 50, 54)
INK = (32, 32, 34)
GREY = (110, 110, 108)
RULE = (150, 140, 115)
COVER = (24, 58, 62)

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- ICAO 9303 check digits ----------
def char_value(ch):
    if ch == "<":
        return 0
    if ch.isdigit():
        return int(ch)
    return ord(ch) - 55  # A=10 .. Z=35

def check_digit(s):
    weights = (7, 3, 1)
    total = 0
    for i, ch in enumerate(s):
        total += char_value(ch) * weights[i % 3]
    return str(total % 10)

def mrz_lines():
    # Line 1: P<KDR + surname + << + given names, padded to 44 with '<'
    line1 = "P<KDRVEYN<<MAREN<ILSA"
    line1 = line1 + "<" * (44 - len(line1))
    # Line 2 (TD3): doc no. + check, nationality, DOB + check, sex,
    # expiry + check, personal number (14 '<') + check, composite check.
    doc = "KD417902<"          # passport no. KD 417 902, padded to 9 chars
    dob = "880612"            # 12 JUN 1988
    exp = "310314"            # 14 MAR 2031
    personal = "<" * 14
    body = (doc + check_digit(doc) + "KDR" + dob + check_digit(dob)
            + "F" + exp + check_digit(exp) + personal + check_digit(personal))
    line2 = body + check_digit(body)
    assert len(line1) == 44 and len(line2) == 44, (len(line1), len(line2))
    return line1, line2

# ---------- helpers ----------
def guilloche(d, x0, y0, x1, y1, color, step=13):
    """Fine wavy horizontal line pattern, clipped to the page rect."""
    for yy in range(y0 + 4, y1 - 2, step):
        pts = []
        for x in range(x0, x1 + 1, 6):
            pts.append((x, yy + 1.1 * math.sin((x - x0) / 26.0 + yy / 9.0)))
        d.line(pts, fill=color, width=1)

def stamp(d, cx, cy, lines, color, angle, w=168, h=86):
    """A rotated rectangular border stamp with centred lines."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    sd.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
                         radius=6, outline=color + (235,), width=2)
    sd.line([cx - w // 2 + 6, cy - h // 2 + 16, cx + w // 2 - 6, cy - h // 2 + 16],
            fill=color + (200,), width=1)
    sd.line([cx - w // 2 + 6, cy + h // 2 - 16, cx + w // 2 - 6, cy + h // 2 - 16],
            fill=color + (200,), width=1)
    f_b = font(SANS_B, 13)
    f_s = font(SANS, 11)
    f_m = font(MONO, 11)
    y = cy - h // 2 + 5
    for i, (txt, kind) in enumerate(lines):
        f = f_b if kind == "b" else (f_m if kind == "m" else f_s)
        tw = sd.textlength(txt, font=f)
        sd.text((cx - tw / 2, y), txt, font=f, fill=color + (240,))
        y += 15 if i == 0 else 14
    layer = layer.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    d._image.alpha_composite(layer)

def draw_portrait(d, x0, y0, x1, y1):
    """Stylised shoulders-up portrait, drawn only with PIL shapes/shading.

    Muted duotone (teal-grey background, warm skin, dark hair) — a
    document-photo treatment, not a pasted face.
    """
    # background: vertical duotone gradient
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, y1 - y0)
        c = tuple(int(168 + (120 - 168) * t) if i == 0 else
                  int(178 + (128 - 178) * t) if i == 1 else
                  int(170 + (122 - 170) * t) for i in range(3))
        d.line([(x0, yy), (x1, yy)], fill=c)
    cx = (x0 + x1) // 2
    # shoulders / jacket (dark teal)
    d.pieslice([cx - 78, y1 - 118, cx + 78, y1 + 60], 180, 360, fill=(38, 62, 66))
    d.polygon([(cx - 78, y1), (cx - 52, y1 - 96), (cx - 18, y1 - 78),
               (cx, y1 - 62), (cx + 18, y1 - 78), (cx + 52, y1 - 96),
               (cx + 78, y1)], fill=(38, 62, 66))
    # collar + shirt V
    d.polygon([(cx - 20, y1 - 76), (cx, y1 - 52), (cx + 20, y1 - 76),
               (cx + 12, y1 - 84), (cx, y1 - 70), (cx - 12, y1 - 84)],
              fill=(232, 224, 205))
    # neck
    d.rectangle([cx - 15, y1 - 128, cx + 15, y1 - 88], fill=(198, 158, 122))
    d.rectangle([cx - 15, y1 - 96, cx + 15, y1 - 88], fill=(178, 138, 104))
    # head
    d.ellipse([cx - 34, y1 - 196, cx + 34, y1 - 112], fill=(206, 166, 130))
    # shading on one side of the face
    d.ellipse([cx + 8, y1 - 194, cx + 34, y1 - 116], fill=(196, 154, 118))
    # ears
    d.ellipse([cx - 40, y1 - 168, cx - 30, y1 - 146], fill=(200, 160, 124))
    d.ellipse([cx + 30, y1 - 168, cx + 40, y1 - 146], fill=(196, 154, 118))
    # hair: dark cap with a side part, drawn over the top of the head
    d.pieslice([cx - 36, y1 - 202, cx + 36, y1 - 128], 180, 360, fill=(52, 44, 40))
    d.polygon([(cx - 36, y1 - 168), (cx - 30, y1 - 196), (cx - 6, y1 - 202),
               (cx + 18, y1 - 196), (cx + 36, y1 - 166), (cx + 30, y1 - 150),
               (cx + 12, y1 - 172), (cx - 8, y1 - 176), (cx - 26, y1 - 162)],
              fill=(52, 44, 40))
    # brows, eyes, nose, mouth — simple, symmetrical, document-photo style
    d.line([(cx - 22, y1 - 162), (cx - 8, y1 - 164)], fill=(70, 56, 48), width=2)
    d.line([(cx + 8, y1 - 164), (cx + 22, y1 - 162)], fill=(70, 56, 48), width=2)
    d.ellipse([cx - 20, y1 - 158, cx - 10, y1 - 152], fill=(250, 246, 236))
    d.ellipse([cx + 10, y1 - 158, cx + 20, y1 - 152], fill=(250, 246, 236))
    d.ellipse([cx - 17, y1 - 157, cx - 13, y1 - 153], fill=(58, 44, 36))
    d.ellipse([cx + 13, y1 - 157, cx + 17, y1 - 153], fill=(58, 44, 36))
    d.line([(cx, y1 - 152), (cx - 2, y1 - 140), (cx + 3, y1 - 139)],
           fill=(178, 138, 104), width=2)
    d.line([(cx - 9, y1 - 130), (cx + 9, y1 - 130)], fill=(150, 96, 84), width=2)
    # soft vignette on the portrait box
    d.rectangle([x0, y0, x1, y1], outline=(90, 80, 60), width=2)

def field(d, x, y, label, value, vfont, label_w=118):
    d.text((x, y), label, font=font(SANS, 10), fill=GREY)
    d.text((x, y + 13), value, font=vfont, fill=INK)

def main():
    img = Image.new("RGBA", (W, H), COVER)
    d = ImageDraw.Draw(img, "RGBA")
    # outer cover border
    d.rectangle([8, 8, W - 9, H - 9], outline=(120, 140, 138), width=1)

    # ---- two cream pages ----
    L = (20, 20, 502, 620)   # left page
    R = (522, 20, 1004, 620)  # right page
    for (x0, y0, x1, y1) in (L, R):
        d.rounded_rectangle([x0, y0, x1, y1], radius=4, fill=CREAM)
        guilloche(d, x0 + 8, y0 + 8, x1 - 8, y1 - 8, (216, 208, 186))
        d.rounded_rectangle([x0, y0, x1, y1], radius=4, outline=(120, 108, 82), width=2)
    # centre spine shadow
    d.rectangle([502, 20, 522, 620], fill=(210, 202, 180))
    d.line([(512, 20), (512, 620)], fill=(150, 138, 108), width=2)

    # ================= LEFT PAGE — data page =================
    lx0, ly0, lx1, ly1 = L
    # small coat-of-arms-ish emblem: mountain peaks in a circle
    ex, ey = lx0 + 34, ly0 + 30
    d.ellipse([ex - 16, ey - 16, ex + 16, ey + 16], outline=TEAL, width=2)
    d.polygon([(ex - 11, ey + 8), (ex - 4, ey - 8), (ex + 1, ey + 2),
               (ex + 5, ey - 5), (ex + 11, ey + 8)], fill=TEAL)
    d.text((lx0 + 60, ly0 + 16), "REPUBLIC OF KALDRIN", font=font(SERIF_B, 21), fill=TEAL)
    d.text((lx0 + 60, ly0 + 42), "PASSPORT  \u00b7  REISEPASS", font=font(SANS_B, 11), fill=TEAL_D)
    d.line([(lx0 + 24, ly0 + 68), (lx1 - 24, ly0 + 68)], fill=RULE, width=1)
    d.text((lx0 + 24, ly0 + 76), "TYPE  P    \u00b7    CODE  KDR    \u00b7    No.  KD 417 902",
           font=font(SANS, 11), fill=INK)

    # portrait box (left) + data fields (right of it)
    px0, py0, px1, py1 = lx0 + 24, ly0 + 102, lx0 + 158, ly0 + 302
    draw_portrait(d, px0, py0, px1, py1)
    d.text((px0, py1 + 5), "PHOTOGRAPH  \u00b7  HOLDER", font=font(SANS, 8), fill=GREY)

    fx = lx0 + 176
    f_bold = font(SERIF_B, 15)
    f_reg = font(SERIF, 14)
    field(d, fx, ly0 + 100, "SURNAME", "VEYN", f_bold)
    field(d, fx, ly0 + 140, "GIVEN NAMES", "MAREN ILSA", f_bold)
    field(d, fx, ly0 + 180, "NATIONALITY", "KALDRINIAN", f_reg)
    field(d, fx, ly0 + 220, "DATE OF BIRTH", "12 JUN 1988", f_reg)
    field(d, fx, ly0 + 260, "PLACE OF BIRTH", "TARNHOLM", f_reg)
    # second column of fields, lower left block
    field(d, lx0 + 24, ly0 + 330, "SEX", "F", f_reg)
    field(d, lx0 + 130, ly0 + 330, "DATE OF ISSUE", "14 MAR 2021", f_reg)
    field(d, lx0 + 300, ly0 + 330, "DATE OF EXPIRY", "14 MAR 2031", f_reg)
    field(d, lx0 + 24, ly0 + 372, "AUTHORITY", "TARNHOLM", f_reg)
    field(d, lx0 + 300, ly0 + 372, "PLACE OF ISSUE", "TARNHOLM", f_reg)
    d.line([(lx0 + 24, ly0 + 416), (lx1 - 24, ly0 + 416)], fill=RULE, width=1)
    # holder signature line
    d.text((lx0 + 24, ly0 + 426), "HOLDER'S SIGNATURE", font=font(SANS, 9), fill=GREY)
    d.text((lx0 + 24, ly0 + 442), "Maren Veyn", font=font(SERIF, 16), fill=(40, 48, 70))
    d.line([(lx0 + 24, ly0 + 464), (lx0 + 200, ly0 + 464)], fill=INK, width=1)
    d.text((lx0 + 300, ly0 + 426), "HEIGHT  168 cm", font=font(SANS, 10), fill=INK)
    d.text((lx0 + 300, ly0 + 446), "EYES  BROWN", font=font(SANS, 10), fill=INK)

    # MRZ
    mrz1, mrz2 = mrz_lines()
    d.rectangle([lx0 + 12, ly1 - 78, lx1 - 12, ly1 - 12], fill=(232, 226, 202))
    mf = font(MONO_B, 15)
    d.text((lx0 + 20, ly1 - 72), mrz1, font=mf, fill=INK)
    d.text((lx0 + 20, ly1 - 50), mrz2, font=mf, fill=INK)
    d.text((lx0 + 24, ly1 - 28), "P<KDR  \u00b7  p. 3", font=font(SANS, 8), fill=GREY)

    # ================= RIGHT PAGE — visas / stamps =================
    rx0, ry0, rx1, ry1 = R
    d.text((rx0 + 24, ry0 + 16), "VISAS", font=font(SERIF_B, 21), fill=TEAL)
    d.text((rx0 + 24, ry0 + 42), "VISA  \u00b7  STAMPS  \u00b7  ENDORSEMENTS", font=font(SANS_B, 10), fill=TEAL_D)
    d.text((rx1 - 60, ry0 + 18), "p. 8\u20139", font=font(SANS, 11), fill=GREY)
    d.line([(rx0 + 24, ry0 + 62), (rx1 - 24, ry0 + 62)], fill=RULE, width=1)

    # bilingual column (telling detail 1): English + Kaldrin line
    d.text((rx0 + 24, ry0 + 72), "KALDRIN \u2014 PASSPORT", font=font(SANS_B, 11), fill=TEAL)
    d.text((rx0 + 24, ry0 + 88), "REISEPASS \u00b7 KALDRIN TORVA L\u00c6ND", font=font(SANS, 11), fill=INK)
    d.text((rx0 + 24, ry0 + 104), "Torva l\u00e6nd, torva fjell \u2014 the valleys keep their own road.",
           font=font(SERIF, 11), fill=(90, 84, 70))

    PURPLE = (104, 62, 128)
    BLUE = (38, 82, 138)
    REDBR = (138, 62, 44)
    # Chronological, all after issue 14 MAR 2021; entry/exit pairs match.
    stamp(d, rx0 + 118, ry0 + 198, [("OSTRAVIA", "b"), ("ENTRY \u00b7 08 APR 2022", "m"),
                                     ("VELGOROD BORDER", "s")], PURPLE, -6)
    stamp(d, rx0 + 330, ry0 + 198, [("OSTRAVIA", "b"), ("EXIT \u00b7 21 APR 2022", "m"),
                                     ("VELGOROD BORDER", "s")], PURPLE, 5)
    stamp(d, rx0 + 118, ry0 + 308, [("MERIDIA", "b"), ("ENTRY \u00b7 17 SEP 2023", "m"),
                                     ("PORT SALENNE", "s")], BLUE, 4)
    stamp(d, rx0 + 330, ry0 + 308, [("MERIDIA", "b"), ("EXIT \u00b7 02 OCT 2023", "m"),
                                     ("PORT SALENNE", "s")], BLUE, -5)
    stamp(d, rx0 + 118, ry0 + 418, [("OSTRAVIA", "b"), ("ENTRY \u00b7 05 JUN 2025", "m"),
                                     ("VELGOROD BORDER", "s")], REDBR, -4)
    stamp(d, rx0 + 330, ry0 + 418, [("OSTRAVIA", "b"), ("EXIT \u00b7 19 JUN 2025", "m"),
                                     ("VELGOROD BORDER", "s")], REDBR, 6)

    # telling paperwork detail: mountain-permit condition stamp
    d.text((rx0 + 24, ry0 + 486), "ENDORSEMENT", font=font(SANS_B, 10), fill=TEAL)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(layer)
    cond = "HIGH VALLEYS PERMIT K-7 REQUIRED BEYOND 2,400 M"
    cf = font(SANS_B, 12)
    cw = sd.textlength(cond, font=cf)
    bx0, by0 = rx0 + 24, ry0 + 504
    sd.rectangle([bx0, by0, bx0 + cw + 16, by0 + 26], outline=REDBR + (235,), width=2)
    sd.text((bx0 + 8, by0 + 6), cond, font=cf, fill=REDBR + (240,))
    layer = layer.rotate(-1.5, resample=Image.BICUBIC, center=(bx0 + cw // 2, by0 + 13))
    d._image.alpha_composite(layer)
    d.text((rx0 + 24, ry0 + 540),
           "Fee stamp: VALLEY PERMIT K-7 \u2014 40 krona, paid 03 JUN 2025, Tarnholm.",
           font=font(SANS, 10), fill=INK)
    d.text((rx0 + 24, ry0 + 558),
           "No stamp in this passport predates its issue, 14 MAR 2021.",
           font=font(SERIF, 11), fill=(90, 84, 70))

    img.convert("RGB").save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"wrote {OUT} {W}x{H} {size} bytes sha256={h}")
    print(f"MRZ: {mrz1}")
    print(f"MRZ: {mrz2}")

if __name__ == "__main__":
    main()
