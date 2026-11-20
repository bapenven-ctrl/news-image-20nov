#!/usr/bin/env python3
"""Renderer for news-image-20261120 — 'FRIDAY 20 NOVEMBER 2026' in one page.
Written fresh for this build session. Deterministic: pure Pillow drawing,
no randomness, no network. Output: entry.png (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W = H = 1024
PAPER = (247, 242, 231)
INK = (10, 10, 10)
NAVY = (16, 32, 54)
GREY = (90, 90, 90)
RULE = (30, 30, 30)

FD = "/usr/share/fonts/truetype/liberation/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
SERIF_B = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"

REGION_COLORS = {
    "ASIA": (31, 111, 178),
    "EUROPE": (106, 63, 160),
    "AMERICAS": (194, 87, 27),
    "MIDEAST": (46, 125, 79),
    "AFRICA": (168, 124, 18),
    "OCEANIA": (14, 124, 134),
    "WORLD": (84, 84, 84),
}

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def tw(font, s):
    return d.textlength(s, font=font)

def fit_lines(text, font, maxw, max_lines):
    """Word-wrap text to maxw; shrink by caller if > max_lines."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(font, t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines[:max_lines], len(lines) > max_lines

def draw_fit(text, x, y, font_name, size, maxw, max_lines, fill=INK, leading=1.12, min_size=8):
    """Draw text, shrinking font until it fits max_lines. Returns y after text."""
    size_now = size
    while size_now >= min_size:
        f = F(font_name, size_now)
        lines, over = fit_lines(text, f, maxw, max_lines)
        if not over:
            break
        size_now -= 1
    f = F(font_name, size_now)
    lines, _ = fit_lines(text, f, maxw, max_lines)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += int(size_now * leading)
    return y

def label_bar(x, y, w, num, place, topic, color, tag=""):
    d.rectangle([x, y, x + w, y + 20], fill=color)
    f = F(SANS_B, 12)
    left = f"{num}  {place} · {topic}"
    d.text((x + 6, y + 4), left, font=f, fill=(255, 255, 255))
    if tag:
        ft = F(SANS_B, 10)
        twd = tw(ft, tag)
        d.rectangle([x + w - twd - 12, y + 3, x + w - 4, y + 17], fill=(255, 255, 255))
        d.text((x + w - twd - 8, y + 5), tag, font=ft, fill=color)

# ---------------------------------------------------------------- scenes
def scene_cyclone(x, y, w, h):
    # sea and sky
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 226))
    sea_y = y + int(h * 0.62)
    d.rectangle([x, sea_y, x + w, y + h], fill=(43, 108, 160))
    # spiral cyclone
    cx, cy, r = x + int(w * 0.30), y + int(h * 0.36), int(h * 0.30)
    for rr, col in [(r, (240, 244, 246)), (int(r * .72), (203, 220, 232)), (int(r * .45), (240, 244, 246)), (int(r * .2), (120, 150, 175))]:
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 200, fill=(90, 110, 130), width=3)
    d.arc([cx - int(r * .7), cy - int(r * .7), cx + int(r * .7), cy + int(r * .7)], 190, 40, fill=(90, 110, 130), width=3)
    # coast + houses on right
    d.polygon([(x + int(w * .58), y + h), (x + int(w * .78), sea_y - 6), (x + w, sea_y + 4), (x + w, y + h)], fill=(214, 186, 130))
    for hx in (0.66, 0.80, 0.90):
        bx = x + int(w * hx); by = sea_y - 16
        d.rectangle([bx, by, bx + 22, by + 16], fill=(150, 84, 52))
        d.polygon([(bx - 3, by), (bx + 11, by - 9), (bx + 25, by)], fill=(96, 52, 32))
    # bent palms
    for px in (0.60, 0.97):
        bx = x + int(w * px); by = y + h - 4
        d.line([bx, by, bx + 3, by - 26], fill=(84, 62, 40), width=3)
        for a in range(5):
            d.arc([bx - 12 + a * 3, by - 40, bx + 16 + a * 3, by - 18], 300, 60, fill=(46, 125, 79), width=2)
    # rain streaks
    for i in range(26):
        rx = x + 8 + (i * 37) % (w - 16); ry = y + 6 + (i * 23) % int(h * 0.5)
        d.line([rx, ry, rx - 5, ry + 11], fill=(70, 110, 150), width=2)
    # waves
    for i in range(7):
        wx = x + 6 + i * int(w / 6.4)
        d.arc([wx, sea_y + 8, wx + 26, sea_y + 22], 180, 360, fill=(220, 238, 250), width=2)

def scene_kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 46))
    gy = y + int(h * 0.78)
    # stars
    for i in range(28):
        sx = x + (i * 53) % w; sy = y + (i * 17) % int(h * 0.4)
        d.point((sx, sy), fill=(220, 224, 235))
    # missile arcs
    for i, fx in enumerate((0.12, 0.30, 0.48, 0.66, 0.84)):
        sx = x + int(w * fx); sy = y + 4
        ex = x + int(w * (fx + 0.16)); ey = gy - 12 - (i % 3) * 8
        d.line([sx, sy, ex, ey], fill=(240, 170, 80), width=2)
        d.line([sx, sy, (sx + ex) // 2, (sy + ey) // 2 - 10], fill=(200, 120, 60), width=1)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 210, 120))
    # explosions
    for fx in (0.24, 0.58, 0.80):
        ex = x + int(w * fx); ey = gy - 16
        for a in range(8):
            import math
            dx = int(13 * math.cos(a * 0.785)); dy = int(10 * math.sin(a * 0.785))
            d.line([ex, ey, ex + dx, ey + dy], fill=(255, 160, 60), width=2)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 190, 90))
    # skyline
    bx = x + 4
    heights = [26, 40, 30, 48, 34, 44, 28, 38, 24, 42, 30]
    i = 0
    while bx < x + w - 18:
        bh = heights[i % len(heights)]
        d.rectangle([bx, gy - bh, bx + 16, gy], fill=(8, 10, 20))
        for wy in range(gy - bh + 4, gy - 4, 8):
            d.point((bx + 5, wy), fill=(250, 220, 130)); d.point((bx + 11, wy + 3), fill=(250, 220, 130))
        bx += 19; i += 1
    # river + bridge with damaged span
    d.rectangle([x, gy, x + w, y + h], fill=(24, 44, 84))
    by = gy + 6
    d.line([x, by, x + int(w * .42), by], fill=(200, 200, 210), width=3)
    d.line([x + int(w * .60), by, x + w, by], fill=(200, 200, 210), width=3)
    d.line([x + int(w * .42), by, x + int(w * .5), by + 8], fill=(200, 200, 210), width=2)
    d.line([x + int(w * .60), by, x + int(w * .52), by + 8], fill=(200, 200, 210), width=2)
    for px in (0.2, 0.75):
        d.line([x + int(w * px), by - 14, x + int(w * px), by], fill=(200, 200, 210), width=2)

def scene_market(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 42, 58))
    # big screens with falling bars (scene, not a chart panel: a trading floor)
    for i, fx in enumerate((0.04, 0.38, 0.70)):
        sx = x + int(w * fx); sw = int(w * 0.27)
        d.rectangle([sx, y + 6, sx + sw, y + int(h * 0.52)], fill=(16, 20, 30), outline=(120, 130, 150))
        base = y + int(h * 0.44)
        for b in range(4):
            bh = int(h * (0.30 - b * 0.055))
            d.rectangle([sx + 6 + b * (sw // 4), base - bh, sx + 6 + b * (sw // 4) + sw // 6, base], fill=(198, 52, 44))
        d.polygon([(sx + sw - 16, y + 12), (sx + sw - 4, y + 12), (sx + sw - 10, y + 20)], fill=(255, 90, 70))
    # floor desks + trader silhouettes
    fy = y + int(h * 0.60)
    for r in range(2):
        dy = fy + r * int(h * 0.19)
        for i in range(5):
            dx = x + 8 + i * int(w / 5)
            d.rectangle([dx, dy + 8, dx + int(w / 5) - 10, dy + 13], fill=(96, 74, 52))
            d.rectangle([dx + 6, dy - 2, dx + 16, dy + 7], fill=(150, 190, 230))
            hx = dx + int(w / 10) - 4
            d.ellipse([hx, dy - 10, hx + 7, dy - 3], fill=(232, 198, 160))
            d.rectangle([hx - 2, dy - 3, hx + 9, dy + 8], fill=(24, 28, 40))

def scene_poland(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(176, 208, 232))
    gy = y + int(h * 0.66)
    d.rectangle([x, gy, x + w, y + h], fill=(126, 160, 84))
    # field rows
    for i in range(3):
        d.line([x, gy + 8 + i * 7, x + w, gy + 2 + i * 7], fill=(100, 132, 62), width=2)
    # crashed missile body
    mx, my = x + int(w * .42), gy + 2
    d.polygon([(mx, my), (mx + 56, my - 8), (mx + 62, my + 2), (mx + 8, my + 9)], fill=(120, 124, 130))
    d.polygon([(mx, my), (mx - 12, my - 6), (mx - 10, my + 8)], fill=(90, 94, 100))
    d.ellipse([mx + 8, my + 6, mx + 66, my + 15], fill=(70, 60, 48))
    # soldiers + tape
    for fx in (0.12, 0.82):
        sx = x + int(w * fx)
        d.ellipse([sx, gy - 14, sx + 7, gy - 7], fill=(232, 198, 160))
        d.rectangle([sx - 1, gy - 7, sx + 8, gy + 6], fill=(70, 84, 54))
    d.line([x + 4, gy - 4, x + w - 4, gy - 10], fill=(240, 200, 40), width=2)
    # polish flag on pole
    px = x + int(w * .9)
    d.line([px, gy - 26, px, gy + 4], fill=(60, 60, 60), width=2)
    d.rectangle([px, gy - 26, px + 16, gy - 20], fill=(245, 245, 245))
    d.rectangle([px, gy - 20, px + 16, gy - 14], fill=(205, 40, 55))

def scene_brussels(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 216, 230))
    d.rectangle([x, y + int(h * .72), x + w, y + h], fill=(150, 120, 88))
    # long table
    ty = y + int(h * .58)
    d.polygon([(x + 14, ty + 14), (x + w - 14, ty + 14), (x + w - 30, ty + 26), (x + 30, ty + 26)], fill=(110, 78, 50))
    d.rectangle([x + 14, ty, x + w - 14, ty + 14], fill=(140, 104, 66))
    # seated figures + handshake centre
    for fx in (0.16, 0.34, 0.66, 0.84):
        sx = x + int(w * fx)
        d.ellipse([sx - 5, ty - 16, sx + 5, ty - 6], fill=(232, 198, 160))
        d.rectangle([sx - 7, ty - 6, sx + 7, ty + 4], fill=(30, 36, 54))
    cx = x + w // 2
    d.line([cx - 12, ty - 4, cx + 2, ty + 2], fill=(232, 198, 160), width=4)
    d.line([cx + 12, ty - 4, cx + 2, ty + 2], fill=(232, 198, 160), width=4)
    # flags: UK left, EU right
    def flag_uk(bx, by):
        d.rectangle([bx, by, bx + 34, by + 22], fill=(30, 50, 130))
        d.line([bx, by, bx + 34, by + 22], fill=(240, 240, 240), width=3)
        d.line([bx + 34, by, bx, by + 22], fill=(240, 240, 240), width=3)
        d.line([bx + 17, by, bx + 17, by + 22], fill=(240, 240, 240), width=5)
        d.line([bx, by + 11, bx + 34, by + 11], fill=(240, 240, 240), width=5)
        d.line([bx + 17, by, bx + 17, by + 22], fill=(200, 40, 50), width=2)
        d.line([bx, by + 11, bx + 34, by + 11], fill=(200, 40, 50), width=2)
    def flag_eu(bx, by):
        d.rectangle([bx, by, bx + 34, by + 22], fill=(30, 60, 160))
        import math
        for i in range(8):
            a = i * 0.785
            sx = bx + 17 + int(7 * math.cos(a)); sy = by + 11 + int(7 * math.sin(a))
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(250, 210, 60))
    flag_uk(x + 10, y + 6)
    flag_eu(x + w - 44, y + 6)
    d.line([x + 27, y + 28, x + 27, ty - 2], fill=(90, 90, 90), width=2)
    d.line([x + w - 27, y + 28, x + w - 27, ty - 2], fill=(90, 90, 90), width=2)

def scene_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    # big screen
    d.rectangle([x + int(w * .18), y + 5, x + int(w * .82), y + int(h * .5)], fill=(24, 60, 90))
    f = F(SANS_B, 12)
    lab = "COP31 · ANTALYA"
    d.text((x + w // 2 - tw(f, lab) / 2, y + 8), lab, font=f, fill=(255, 255, 255))
    # delegate rows
    for r in range(2):
        ry = y + int(h * .62) + r * int(h * .18)
        for i in range(6):
            sx = x + 10 + i * int(w / 6)
            d.ellipse([sx, ry, sx + 7, ry + 7], fill=(232, 198, 160))
            d.rectangle([sx - 2, ry + 7, sx + 9, ry + 13], fill=(52, 62, 84))
        d.rectangle([x + 4, ry + 12, x + w - 4, ry + 15], fill=(150, 120, 88))

def scene_saudi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 214, 160))
    gy = y + int(h * .8)
    d.rectangle([x, gy, x + w, y + h], fill=(216, 178, 116))
    # dunes
    d.arc([x - 10, gy - 12, x + int(w * .5), gy + 10], 180, 360, fill=(190, 150, 92), width=2)
    d.arc([x + int(w * .45), gy - 10, x + w + 8, gy + 12], 180, 360, fill=(190, 150, 92), width=2)
    # incoming missile + interceptor + burst
    d.line([x + 8, y + 6, x + int(w * .52), y + int(h * .42)], fill=(120, 60, 40), width=2)
    d.polygon([(x + int(w * .52), y + int(h * .42)), (x + int(w * .46), y + int(h * .34)), (x + int(w * .58), y + int(h * .36))], fill=(150, 60, 40))
    d.line([x + int(w * .8), gy - 4, x + int(w * .56), y + int(h * .44)], fill=(70, 90, 120), width=2)
    ex, ey = x + int(w * .55), y + int(h * .42)
    import math
    for a in range(10):
        dx = int(14 * math.cos(a * .628)); dy = int(11 * math.sin(a * .628))
        d.line([ex, ey, ex + dx, ey + dy], fill=(230, 120, 30), width=2)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 200, 90))
    # radar dome + launcher
    d.pieslice([x + int(w * .78), gy - 18, x + int(w * .94), gy + 2], 180, 360, fill=(235, 235, 235), outline=(150, 150, 150))
    d.rectangle([x + int(w * .08), gy - 8, x + int(w * .2), gy], fill=(90, 96, 80))
    d.line([x + int(w * .14), gy - 8, x + int(w * .3), gy - 20], fill=(90, 96, 80), width=3)

def scene_iraq(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 178))
    gy = y + int(h * .78)
    d.rectangle([x, gy, x + w, y + h], fill=(198, 168, 118))
    # compound wall + gate
    d.rectangle([x + int(w * .55), y + int(h * .18), x + w - 6, gy], fill=(176, 148, 104))
    d.rectangle([x + int(w * .55), y + int(h * .18), x + w - 6, y + int(h * .26)], fill=(150, 122, 80))
    d.rectangle([x + int(w * .68), gy - 22, x + int(w * .8), gy], fill=(60, 54, 44))
    # palm
    px = x + int(w * .9)
    d.line([px, gy, px + 2, gy - 30], fill=(100, 78, 46), width=3)
    for a in range(5):
        d.arc([px - 14 + a * 4, gy - 44, px + 12 + a * 4, gy - 26], 300, 60, fill=(60, 120, 66), width=2)
    # armoured vehicles convoy
    for i, fx in enumerate((0.04, 0.26)):
        vx = x + int(w * fx); vy = gy - 14
        d.rectangle([vx, vy, vx + 34, vy + 10], fill=(96, 102, 78))
        d.rectangle([vx + 8, vy - 6, vx + 24, vy], fill=(96, 102, 78))
        d.line([vx + 24, vy - 4, vx + 34, vy - 8], fill=(70, 74, 58), width=2)
        d.ellipse([vx + 4, vy + 8, vx + 12, vy + 15], fill=(40, 40, 40))
        d.ellipse([vx + 22, vy + 8, vx + 30, vy + 15], fill=(40, 40, 40))

def scene_delhi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    gy = y + int(h * .8)
    # red carpet
    d.polygon([(x + int(w * .3), y + h), (x + int(w * .46), gy), (x + int(w * .6), gy), (x + int(w * .78), y + h)], fill=(178, 40, 52))
    # plane tail behind
    d.polygon([(x + int(w * .06), gy - 34), (x + int(w * .2), gy - 34), (x + int(w * .14), gy - 52)], fill=(230, 230, 235), outline=(140, 150, 165))
    # minister figure walking
    mx = x + int(w * .5)
    d.ellipse([mx - 5, gy - 34, mx + 5, gy - 24], fill=(150, 108, 74))
    d.rectangle([mx - 6, gy - 24, mx + 6, gy - 8], fill=(34, 40, 60))
    d.line([mx - 3, gy - 8, mx - 6, gy + 2], fill=(34, 40, 60), width=3)
    d.line([mx + 3, gy - 8, mx + 7, gy + 2], fill=(34, 40, 60), width=3)
    # flags India & Pakistan
    def flag_in(bx, by):
        d.rectangle([bx, by, bx + 26, by + 6], fill=(240, 140, 50))
        d.rectangle([bx, by + 6, bx + 26, by + 12], fill=(245, 245, 245))
        d.rectangle([bx, by + 12, bx + 26, by + 18], fill=(40, 140, 70))
        d.ellipse([bx + 11, by + 7, bx + 15, by + 11], outline=(40, 60, 160))
    def flag_pk(bx, by):
        d.rectangle([bx, by, bx + 26, by + 18], fill=(20, 100, 55))
        d.rectangle([bx, by, bx + 6, by + 18], fill=(245, 245, 245))
        d.ellipse([bx + 14, by + 5, bx + 21, by + 12], fill=(245, 245, 245))
        d.ellipse([bx + 16, by + 4, bx + 23, by + 11], fill=(20, 100, 55))
    flag_in(x + 8, y + 6); flag_pk(x + w - 34, y + 6)
    d.line([x + 21, y + 24, x + 21, gy - 4], fill=(90, 90, 90), width=2)
    d.line([x + w - 21, y + 24, x + w - 21, gy - 4], fill=(90, 90, 90), width=2)

def scene_signal(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 226, 244))
    # phone
    px, py, pw, ph = x + int(w * .36), y + 4, int(w * .28), int(h * .92)
    d.rounded_rectangle([px, py, px + pw, py + ph], 7, fill=(28, 32, 44))
    d.rectangle([px + 4, py + 8, px + pw - 4, py + ph - 6], fill=(238, 244, 250))
    # chat bubbles
    for i, (bw_, side) in enumerate(((0.6, 0), (0.45, 1), (0.55, 0))):
        by = py + 13 + i * int(ph * .22)
        bw2 = int((pw - 12) * bw_)
        bx = px + 7 if side == 0 else px + pw - 7 - bw2
        d.rounded_rectangle([bx, by, bx + bw2, by + 9], 3, fill=(120, 180, 240) if side == 0 else (170, 220, 170))
    # crossed eye / shield
    cx, cy = px + pw // 2, py + int(ph * .8)
    d.ellipse([cx - 11, cy - 6, cx + 11, cy + 6], outline=(190, 40, 40), width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(190, 40, 40))
    d.line([cx - 12, cy + 7, cx + 12, cy - 7], fill=(190, 40, 40), width=2)
    # robot head peeking, blocked
    rx = x + int(w * .74)
    d.rounded_rectangle([rx, y + int(h * .3), rx + 26, y + int(h * .62)], 5, fill=(150, 158, 170))
    d.ellipse([rx + 6, y + int(h * .42), rx + 11, y + int(h * .5)], fill=(30, 34, 44))
    d.ellipse([rx + 15, y + int(h * .42), rx + 20, y + int(h * .5)], fill=(30, 34, 44))
    d.line([rx - 4, y + int(h * .24), rx + 30, y + int(h * .68)], fill=(190, 40, 40), width=3)

def scene_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 208, 160))
    gy = y + int(h * .8)
    d.rectangle([x, gy, x + w, y + h], fill=(196, 172, 110))
    # stadium arc
    d.arc([x - 20, y - int(h * .5), x + w + 20, y + int(h * .55)], 20, 160, fill=(240, 240, 240), width=5)
    d.arc([x - 20, y - int(h * .42), x + w + 20, y + int(h * .6)], 20, 160, fill=(200, 60, 60), width=3)
    # batsman
    bx = x + int(w * .42)
    d.ellipse([bx, gy - 34, bx + 9, gy - 25], fill=(120, 82, 54))
    d.rectangle([bx + 1, gy - 25, bx + 9, gy - 10], fill=(240, 240, 245))
    d.line([bx + 8, gy - 22, bx + 22, gy - 34], fill=(120, 82, 54), width=3)  # bat arm
    d.line([bx + 20, gy - 36, bx + 28, gy - 20], fill=(196, 164, 100), width=3)  # bat
    d.line([bx + 3, gy - 10, bx - 2, gy], fill=(240, 240, 245), width=3)
    d.line([bx + 7, gy - 10, bx + 13, gy], fill=(240, 240, 245), width=3)
    # ball + stumps
    d.ellipse([x + int(w * .68), gy - 30, x + int(w * .68) + 6, gy - 24], fill=(200, 40, 40))
    sx = x + int(w * .82)
    for i in range(3):
        d.rectangle([sx + i * 5, gy - 16, sx + i * 5 + 2, gy], fill=(230, 200, 90))

def scene_shenzhen(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 220, 236))
    # skyline
    for i, bh in enumerate((30, 44, 26, 50, 34)):
        bx = x + 6 + i * int(w / 5)
        d.rectangle([bx, y + h - 14 - bh, bx + int(w / 5) - 8, y + h - 14], fill=(140, 160, 185))
    gy = y + h - 12
    d.rectangle([x, gy, x + w, y + h], fill=(120, 110, 96))
    # table + two leaders
    ty = y + int(h * .52)
    d.rectangle([x + int(w * .18), ty + 12, x + int(w * .82), ty + 20], fill=(110, 78, 50))
    for fx in (0.32, 0.68):
        sx = x + int(w * fx)
        d.ellipse([sx - 6, ty - 12, sx + 6, ty], fill=(232, 198, 160) if fx < .5 else (198, 152, 108))
        d.rectangle([sx - 8, ty, sx + 8, ty + 13], fill=(34, 40, 60))
    # flags China & Indonesia
    def flag_cn(bx, by):
        d.rectangle([bx, by, bx + 26, by + 18], fill=(215, 40, 45))
        d.polygon([(bx + 5, by + 3), (bx + 6.5, by + 6), (bx + 9, by + 6), (bx + 7, by + 7.6), (bx + 8, by + 10), (bx + 5, by + 8.6), (bx + 2, by + 10), (bx + 3, by + 7.6), (bx + 1, by + 6), (bx + 3.5, by + 6)], fill=(250, 220, 60))
    def flag_id(bx, by):
        d.rectangle([bx, by, bx + 26, by + 9], fill=(215, 40, 45))
        d.rectangle([bx, by + 9, bx + 26, by + 18], fill=(245, 245, 245))
    flag_cn(x + 8, y + 5); flag_id(x + w - 34, y + 5)
    d.line([x + 21, y + 23, x + 21, ty - 2], fill=(90, 90, 90), width=2)
    d.line([x + w - 21, y + 23, x + w - 21, ty - 2], fill=(90, 90, 90), width=2)

def scene_seoul(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 226, 232))
    # courthouse
    cx = x + w // 2
    d.polygon([(cx - int(w * .34), y + 14), (cx, y + 2), (cx + int(w * .34), y + 14)], fill=(110, 116, 128))
    d.rectangle([x + int(w * .14), y + 16, x + int(w * .86), y + 20], fill=(130, 136, 148))
    for i in range(4):
        bx = x + int(w * (.2 + i * .16))
        d.rectangle([bx, y + 22, bx + 8, y + int(h * .62)], fill=(238, 240, 244), outline=(150, 154, 164))
    d.rectangle([x + int(w * .12), y + int(h * .62), x + int(w * .88), y + int(h * .68)], fill=(130, 136, 148))
    # gavel
    gx, gy = cx + int(w * .18), y + int(h * .8)
    d.line([gx, gy, gx + 18, gy - 12], fill=(120, 84, 46), width=4)
    d.rectangle([gx + 12, gy - 18, gx + 24, gy - 10], fill=(150, 106, 58))
    d.rectangle([gx - 8, gy + 3, gx + 16, gy + 6], fill=(110, 78, 44))
    # scales left
    sx = cx - int(w * .24); sy = y + int(h * .78)
    d.line([sx, sy - 22, sx, sy], fill=(90, 90, 90), width=2)
    d.line([sx - 12, sy - 20, sx + 12, sy - 20], fill=(90, 90, 90), width=2)
    for sgn in (-1, 1):
        px = sx + sgn * 12
        d.line([px, sy - 20, px - 5, sy - 10], fill=(90, 90, 90), width=1)
        d.line([px, sy - 20, px + 5, sy - 10], fill=(90, 90, 90), width=1)
        d.arc([px - 6, sy - 13, px + 6, sy - 5], 0, 180, fill=(90, 90, 90), width=2)

# ---------------------------------------------------------------- data
HEROES = [
    dict(num=1, place="GOPALPUR", topic="CYCLONE", region="ASIA", scene=scene_cyclone,
         headline="Cyclone Akvan makes landfall in eastern India",
         summary="Akvan crossed the Odisha coast at 70–80 km/h, gusting 90. 370,000 evacuated; no major damage reported.",
         source="IMD · THE HINDU", tag=""),
    dict(num=2, place="KYIV", topic="WAR", region="EUROPE", scene=scene_kyiv,
         headline="Russia fires 110+ missiles at Kyiv; three bridges damaged",
         summary="110+ missiles and ~400 drones overnight: eight dead, 28 hurt, three Dnipro bridges hit.",
         source="CNN · REUTERS", tag=""),
    dict(num=3, place="TOKYO", topic="MARKETS", region="ASIA", scene=scene_market,
         headline="Asia's AI rout deepens at Friday's close",
         summary="Nikkei −5.1%, KOSPI −5.2%, SoftBank −16% — a Friday session, not Thursday's US falls.",
         source="REUTERS", tag=""),
]
CARDS = [
    dict(num=4, place="NOWY LIPOWIEC", topic="NATO", region="EUROPE", scene=scene_poland,
         headline="Russian cruise missile crashes in Poland",
         summary="Warsaw says a Kh-101 came down near the border. No casualties.",
         source="REUTERS", tag=""),
    dict(num=5, place="BRUSSELS", topic="EUROPE", region="EUROPE", scene=scene_brussels,
         headline="UK and EU agree Brexit reset deal",
         summary="Youth mobility for 100,000 a year, a food deal, linked carbon markets.",
         source="REUTERS", tag=""),
    dict(num=6, place="ANTALYA", topic="CLIMATE", region="WORLD", scene=scene_cop,
         headline="COP31 reaches its final day with no deal",
         summary="The draft drops fossil fuels and the $120bn figure; overtime looms.",
         source="AFP · REUTERS", tag=""),
    dict(num=7, place="JAZAN", topic="MIDDLE EAST", region="MIDEAST", scene=scene_saudi,
         headline="Saudi defences intercept Houthi missile",
         summary="A ballistic missile was destroyed over the south; strikes on Sanaa reported.",
         source="REUTERS", tag="CLAIM"),
    dict(num=8, place="BAGHDAD", topic="IRAQ", region="MIDEAST", scene=scene_iraq,
         headline="Iraqi forces deploy into militia stronghold",
         summary="Troops entered Jurf al-Sakhar under a compromise deal.",
         source="REUTERS", tag=""),
    dict(num=9, place="NEW DELHI", topic="DIPLOMACY", region="ASIA", scene=scene_delhi,
         headline="Pakistan minister in India, first since 2025 war",
         summary="Musadik Malik arrived for the SCO dialogue forum in New Delhi.",
         source="AL JAZEERA", tag=""),
    dict(num=10, place="SIGNAL", topic="TECHNOLOGY", region="WORLD", scene=scene_signal,
         headline="Signal blocks screenshots to stop AI agents",
         summary="Screenshots restricted by default so AI agents cannot read chats.",
         source="REUTERS", tag=""),
    dict(num=11, place="RAWALPINDI", topic="CRICKET", region="ASIA", scene=scene_cricket,
         headline="Pakistan beat Sri Lanka to take the series",
         summary="Pakistan chased 90 to win by 8 wickets; the series ends 1–0.",
         source="REUTERS", tag=""),
    dict(num=12, place="SHENZHEN", topic="ASIA", region="ASIA", scene=scene_shenzhen,
         headline="Prabowo meets Xi in Shenzhen",
         summary="Economic partnership and South China Sea cooperation discussed.",
         source="REUTERS", tag=""),
    dict(num=13, place="SEOUL", topic="POLITICS", region="ASIA", scene=scene_seoul,
         headline="Ruling party adopts impeaching chief justice",
         summary="Impeaching Chief Justice Cho is now official party policy.",
         source="YONHAP", tag=""),
]
BRIEFS = [
    (14, "Tallinn", "Estonia says its Russia border closure from 1 Dec will last at least six months. (Reuters)"),
    (15, "Geneva", "WFP cuts its 2027 aid target to 91 million people on a $12bn appeal. (Reuters)"),
    (16, "Moscow", "Russia's defence ministry claims hits on Odesa port and a cargo vessel. (Reuters) CLAIM"),
    (17, "Bangkok", "PM Anutin defends the US trade deal: Thailand must keep America a major partner. (Reuters)"),
    (18, "Copenhagen", "Equinor says a cyberattack on the company has been stopped; no output hit. (Reuters)"),
    (19, "Sydney", "A man of 35 is charged with terror offences over alleged car-bomb research. (Reuters)"),
    (20, "Tokyo", "Japan's October inflation printed 2.3%, core 2.2%, in data released Friday. (Dow Jones)"),
    (21, "Beijing", "China holds lending rates for an 18th month: 1-year 3.0%, 5-year 3.5%. (Reuters)"),
    (22, "London", "UK retail sales rose 0.7% in October, beating every forecast. (Reuters · ONS)"),
    (23, "Frankfurt", "STOXX 600 fell 1% on Friday morning, heading for its worst week since March. (Reuters)"),
    (24, "Sydney", "ASX 200 closed −1.6% for a seventh straight loss; worst week since 2022. (WSJ)"),
    (25, "London", "Brent slipped to $91.03 on Friday, set for a third straight weekly decline. (Reuters)"),
    (26, "Markets", "Gold slid on Friday toward a 7–8% weekly loss, near $3,600 an ounce. (Reuters)"),
    (27, "New York", "Anthropic fell 6% in Friday premarket to $91.24 — a post-debut reality check. (Reuters)"),
    (28, "Jakarta", "CreditSights warns mining-policy uncertainty is raising cost pressures. (Reuters)"),
    (29, "Melbourne", "David Jones tells 1,680 staff their jobs end just after Christmas. (The West)"),
    (30, "Landes", "Cargo ship MIRO G runs aground off France; 19 crew airlifted to safety. (Reuters)"),
    (31, "Loyalty Is.", "M5.6 quake southeast of the Loyalty Islands at 00:49 UTC; no tsunami threat. (USGS)"),
    (32, "Madang", "M5.1 quake near Madang, Papua New Guinea, at 05:17 UTC; felt by ~810,000. (GFZ)"),
    (33, "Florida", "Flash flood warning for Brevard County after 2.5 inches of rain. (NWS)"),
    (34, "Orbit", "SpaceX Dragon due to undock the ISS Friday with 6,300 lb of science. (NASA)"),
    (35, "Global", "Tire chemicals found in human bodies on four continents, a review finds. (ACS)"),
    (36, "Pretoria", "581 women were killed in South Africa in July–September, Friday's statistics show. (BBC)"),
    (37, "Lesotho", "11 arrested at the border gate, incl. officials and police, in a graft probe. (SAnews)"),
    (38, "Busia", "Kenya's Ruto mocks the opposition after its walkout from an IEBC meeting. (People Daily)"),
    (39, "Ohio", "E. coli outbreak at Ohio University grows to 17 confirmed cases, all students. (FSN)"),
    (40, "Basel", "BioVersys reports Phase 2a results for its AlpE tuberculosis regimen. (BioVersys)"),
    (41, "Sydney", "Marathon champion Jepchirchir is banned 3 years for doping; Sydney title stripped. (ABC)"),
    (42, "Antalya", "Host Turkey banks $26bn in side deals as COP31 diplomacy stalls. (Reuters)"),
    (43, "Bhubaneswar", "Odisha's assembly is adjourned until 23 Nov because of Cyclone Akvan. (Indian press)"),
    (44, "Surabaya", "Officers at Juanda stop two Indonesians suspected of leaving to fight for Russia."),
    (45, "Global", "GTA VI: The Album is released Friday with 34 original tracks. (Our Culture) CLAIM"),
]
FIGURES = [
    ("370,000", "evacuated ahead of Cyclone Akvan"),
    ("110+", "missiles fired at Ukraine overnight"),
    ("−5.1%", "Nikkei 225 at Friday's close"),
    ("209 mm", "of rain at Patrapur, Odisha"),
    ("$12bn", "WFP food appeal for 2027"),
]
EXCLUSIONS = ("Checked and NOT shown as Friday's news — Trump–Iran 'decision can wait to 2027' interviews (Thu 19 Nov) · Voyager 1's one light-day (Wed 18 Nov) · "
              "Houthi strike on Riyadh's PIF Tower (Thu 19) · ICJ Myanmar genocide ruling (Thu 19) · Trump–Xi–Putin Shenzhen trilateral (Thu 19) · "
              "Anthropic's +17% debut close (Thu 19) · US Thursday selloff, Dow −1,101 (Thu 19) · Putin's Kerch vow (Thu 19) · Hormuz tanker mines (Thu 19) · "
              "Hayabusa2 retargeting (Tue 17) · Fiji disaster declaration (Wed 18) · Han Duck-soo ruling (Thu 19) · Senegal migrant boat (Wed 18) · Fiona the hippo (Thu 19)")

# ---------------------------------------------------------------- layout
MX = 16
CW = W - 2 * MX  # 992

# masthead
f = F(SANS_B, 12)
d.text((MX, 12), "THE WORLD IN ONE PAGE", font=f, fill=INK)
r = "45 STORIES · ALL DATED FRI 20 NOV"
d.text((W - MX - tw(f, r), 12), r, font=f, fill=INK)
d.line([MX, 27, W - MX, 27], fill=RULE, width=2)
draw_fit("FRIDAY 20 NOVEMBER 2026", MX, 33, SERIF_B, 50, CW, 1, fill=INK)
d.line([MX, 88, W - MX, 88], fill=RULE, width=2)

# region bar (counts from data)
from collections import Counter
cnt = Counter()
for p in HEROES + CARDS:
    cnt[p["region"]] += 1
brief_regions = ["EUROPE", "WORLD", "EUROPE", "ASIA", "EUROPE", "OCEANIA", "ASIA", "ASIA", "EUROPE", "EUROPE",
                 "OCEANIA", "WORLD", "WORLD", "AMERICAS", "ASIA", "OCEANIA", "EUROPE", "OCEANIA", "OCEANIA",
                 "AMERICAS", "WORLD", "WORLD", "AFRICA", "AFRICA", "AFRICA", "AMERICAS", "EUROPE", "AFRICA",
                 "MIDEAST", "ASIA", "ASIA", "WORLD"]
assert len(brief_regions) == len(BRIEFS) == 32, (len(brief_regions), len(BRIEFS))
for rgn in brief_regions:
    cnt[rgn] += 1
order = ["ASIA", "EUROPE", "AMERICAS", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]
names = {"ASIA": "ASIA-PACIFIC", "EUROPE": "EUROPE", "AMERICAS": "AMERICAS", "MIDEAST": "MIDEAST",
         "AFRICA": "AFRICA", "OCEANIA": "OCEANIA", "WORLD": "WORLD / SPACE"}
total = sum(cnt[o] for o in order)
x = MX
ybar = 96
for o in order:
    wseg = int(CW * cnt[o] / total)
    d.rectangle([x, ybar, x + wseg, ybar + 20], fill=REGION_COLORS[o])
    lab = f"{names[o]} {cnt[o]}"
    for _sz in (11, 10, 9, 8):
        fl = F(SANS_B, _sz)
        if tw(fl, lab) < wseg - 4:
            d.text((x + (wseg - tw(fl, lab)) / 2, ybar + 5), lab, font=fl, fill=(255, 255, 255))
            break
    x += wseg

# figures row (caption ends ~yfig+49; rule below at 182 keeps 9px clear — no strike-through)
yfig = 124
fw = CW // 5
for i, (num, cap) in enumerate(FIGURES):
    fx = MX + i * fw
    if i:
        d.line([fx - 6, yfig + 2, fx - 6, yfig + 38], fill=(180, 170, 150), width=1)
    draw_fit(num, fx, yfig, SERIF_B, 22, fw - 12, 1, fill=(150, 40, 30) if i in (1, 2) else INK)
    draw_fit(cap, fx, yfig + 28, SANS, 10, fw - 12, 2, fill=GREY, leading=1.05)
d.line([MX, 182, W - MX, 182], fill=RULE, width=2)

# heroes: y 192..386 (194 tall, 10px margin above from rule at 182), widths 4:3:3
HY, HH = 192, 194
gaps = 12
usable = CW - 2 * gaps
hw = [int(usable * 0.4), int(usable * 0.3), usable - int(usable * 0.4) - int(usable * 0.3)]
x = MX
for p, wpx in zip(HEROES, hw):
    d.rectangle([x, HY, x + wpx, HY + HH], fill=(255, 255, 255), outline=(120, 120, 120))
    label_bar(x, HY, wpx, p["num"], p["place"], p["topic"], REGION_COLORS[p["region"]], p["tag"])
    iy = HY + 24
    ih = 92
    p["scene"](x + 3, iy, wpx - 6, ih)
    ty = iy + ih + 4
    ty = draw_fit(p["headline"], x + 7, ty, SERIF_B, 18, wpx - 14, 2, leading=1.06)
    ty = draw_fit(p["summary"], x + 7, ty + 1, SERIF, 10, wpx - 14, 2, leading=1.1)
    d.text((x + 7, HY + HH - 14), p["source"], font=F(SANS_B, 9), fill=(150, 40, 30))
    x += wpx + gaps

# cards: two rows of five, y 398.. and 550.., 140 tall, 12px margin above each row
CY = 398
CHH = 140
cgap = 10
cw5 = (CW - 4 * cgap) // 5
for row in range(2):
    y = CY + row * (CHH + 12)
    for col in range(5):
        p = CARDS[row * 5 + col]
        x = MX + col * (cw5 + cgap)
        d.rectangle([x, y, x + cw5, y + CHH], fill=(255, 255, 255), outline=(120, 120, 120))
        label_bar(x, y, cw5, p["num"], p["place"], p["topic"], REGION_COLORS[p["region"]], p["tag"])
        iy = y + 23
        ih = 54
        p["scene"](x + 3, iy, cw5 - 6, ih)
        ty = iy + ih + 3
        ty = draw_fit(p["headline"], x + 6, ty, SERIF_B, 12, cw5 - 12, 2, leading=1.06)
        draw_fit(p["summary"], x + 6, ty + 1, SERIF, 9, cw5 - 12, 2, leading=1.08)
        d.text((x + 6, y + CHH - 12), p["source"], font=F(SANS_B, 8), fill=(150, 40, 30))

# bottom band: map left, briefs right — y 706..954 (rule at 700, 10px below cards)
BY, BH = 706, 248
d.line([MX, BY - 6, W - MX, BY - 6], fill=RULE, width=2)
MAPW = 296
d.rectangle([MX, BY, MX + MAPW, BY + BH], fill=(233, 238, 244), outline=(120, 120, 120))
d.text((MX + 8, BY + 6), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
# dotted world map from a coarse land grid
LAND = [
    "                                                                ",
    "  oooooooo          oooo           ooooooooooooooooooooooo      ",
    " oooooooooooo      o  ooo      oooooooooooooooooooooooooooooo   ",
    "oooooooooooooo        ooooo  ooooooooooooooooooooooooooooooooo  ",
    " oooooooooooo         oooooo ooooooooooooooooooooooooooo  oo  ",
    "  oooooooooo           oooooooooooooooooooooooooooooooooooo     ",
    "   oooooooo             ooooooooooooooooooooooooooooooooo       ",
    "    ooooo       ooo      oooooooooooooooooooooooooooooo         ",
    "                ooooo     oooooooooooooooooooooooooooo          ",
    "                oooooo     ooooooooooooooooooooooooo            ",
    "                ooooo      oooooooooo      oooooooo             ",
    "                 oooo       oooooooo        oooooooo            ",
    "                 ooo         ooooo           ooooooooo          ",
    "                  o           ooo             ooooooo        o  ",
    "                                                                ",
]
LAND = [_r.ljust(64)[:64] for _r in LAND]
gx0, gy0 = MX + 8, BY + 28
cell = 4.3
for ri, rowtxt in enumerate(LAND):
    for ci, ch in enumerate(rowtxt):
        if ch == "o":
            px = gx0 + ci * cell; py = gy0 + ri * cell
            d.ellipse([px, py, px + 2.4, py + 2.4], fill=(110, 140, 170))
# pins for illustrated stories: (num, grid col, grid row)
PINS = [(1, 41, 7), (2, 31, 3), (3, 57, 4), (4, 29, 3), (5, 27, 3), (6, 33, 5), (7, 37, 6),
        (8, 35, 5), (9, 40, 6), (10, 2, 5), (11, 39, 5), (12, 49, 6), (13, 53, 4)]
fp = F(SANS_B, 9)
for num, ci, ri in PINS:
    px = gx0 + ci * cell; py = gy0 + ri * cell
    d.ellipse([px - 5, py - 5, px + 6, py + 6], fill=(190, 40, 40))
    s = str(num)
    d.text((px - tw(fp, s) / 2, py - 5), s, font=fp, fill=(255, 255, 255))
tl_y = BY + 104
d.text((MX + 8, tl_y), "FRIDAY IN UTC", font=F(SANS_B, 10), fill=INK)
draw_fit("00:49 Loyalty Islands quake M5.6 · 01:15 China holds lending rates · 02:00 Akvan crosses the Odisha coast · "
         "06:00 Tokyo closes −5.1% · 07:00 UK retail sales +0.7% · 10:00 Mumbai closes +898 points · 17:05 Dragon due to undock the ISS",
         MX + 8, tl_y + 14, SANS, 9, MAPW - 16, 6, fill=(40, 40, 40), leading=1.25)
d.text((MX + 8, BY + BH - 18), "Pins mark stories 1–13. Briefs 14–45 at right.", font=F(SANS, 9), fill=GREY)

# briefs: 3 columns x 12
BX = MX + MAPW + 12
BW3 = (W - MX - BX - 2 * 10) // 3
d.text((BX, BY + 2), "MORE NEWS — 32 MORE STORIES", font=F(SANS_B, 13), fill=INK)
d.line([BX, BY + 20, W - MX, BY + 20], fill=RULE, width=1)
per_col = 11
for i, (num, city, text) in enumerate(BRIEFS):
    col = i // per_col; row = i % per_col
    bx = BX + col * (BW3 + 10)
    by = BY + 26 + row * 20
    head = f"{num} · {city} — "
    fb = F(SANS_B, 9)
    d.text((bx, by), head, font=fb, fill=INK)
    # wrap full text into 2 lines of column width
    full = head + text
    lines, _ = fit_lines(full, F(SANS, 9), BW3, 2)
    # redraw cleanly: first line bold head + regular rest is complex; use regular with bold head overlay
    d.rectangle([bx, by, bx + BW3, by + 18], fill=PAPER)
    yy = by
    first = True
    for ln in lines:
        d.text((bx, yy), ln, font=F(SANS, 9), fill=(30, 30, 30))
        yy += 9.5
    d.text((bx, by), head, font=fb, fill=INK)

# date check band — 3 style variants (DATECHECK env): dark (current), cream, red
DY = 962
DC_STYLE = os.environ.get("DATECHECK", "dark")
DC_STYLES = {
    # v1 "hitam": deep navy band, white title, pale body (perlakuan saat ini)
    "dark":  dict(fill=NAVY, outline=None, title=(255, 255, 255), body=(210, 218, 230)),
    # v2 "krem": nada kertas masthead, teks tinta gelap, bingkai garis tegas
    "cream": dict(fill=(252, 248, 238), outline=RULE, title=INK, body=(45, 45, 45)),
    # v3 "merah aksen": merah tua yang sama dengan angka figur & label sumber
    "red":   dict(fill=(150, 40, 30), outline=None, title=(255, 255, 255), body=(252, 228, 218)),
}
dc = DC_STYLES[DC_STYLE]
d.rectangle([MX, DY, W - MX, DY + 48], fill=dc["fill"], outline=dc["outline"], width=2 if dc["outline"] else 1)
d.text((MX + 8, DY + 5), "DATE CHECK — Every story above happened, or was first reported, on Friday 20 November 2026, in at least one time zone.",
       font=F(SANS_B, 10), fill=dc["title"])
draw_fit(EXCLUSIONS, MX + 8, DY + 19, SANS, 8, CW - 16, 3, fill=dc["body"], leading=1.15)
d.text((MX, H - 10), "Sources: Reuters · AP · AFP · Al Jazeera · CNN · IMD · BBC · Yonhap · USGS. Original flat illustrations.",
       font=F(SANS, 8), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.environ.get("OUT_PNG", "entry.png"))
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
