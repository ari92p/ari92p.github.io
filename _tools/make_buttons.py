"""Draws the menu buttons and the red arrow as small low-resolution pixel images.

Run:  python3 _tools/make_buttons.py
Output: static/img/btn-*.png (63x53) and static/img/arrow.png (32x24). No dependencies.
The pictures are shown with image-rendering: pixelated, so every pixel stays a hard square.
"""
import math, os, struct, zlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "img")
W, H = 63, 53

FACE = [(61, 129, 152), (83, 191, 213), (108, 221, 253), (117, 251, 254)]
BEV_TOP = [(102, 222, 244), (73, 166, 173)]
BEV_LEFT = [(81, 152, 199), (66, 111, 160)]
BEV_BOTTOM = [(32, 73, 86), (22, 46, 64)]
BEV_RIGHT = [(32, 73, 86), (22, 46, 64)]
ICON_MAIN, ICON_LIGHT, ICON_DARK = (84, 134, 163), (200, 240, 250), (31, 77, 99)
WHITE, OUTLINE = (255, 255, 255), (16, 56, 74)
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

FONT = {
 "N": "10001 11001 10101 10101 10011 10001 10001", "E": "11111 10000 10000 11110 10000 10000 11111",
 "W": "10001 10001 10001 10101 10101 11011 10001", "S": "01111 10000 10000 01110 00001 00001 11110",
 "P": "11110 10001 10001 11110 10000 10000 10000", "R": "11110 10001 10001 11110 10100 10010 10001",
 "O": "01110 10001 10001 10001 10001 10001 01110", "J": "00111 00010 00010 00010 00010 10010 01100",
 "C": "01110 10001 10000 10000 10000 10001 01110", "T": "11111 00100 00100 00100 00100 00100 00100",
 "B": "11110 10001 10001 11110 10001 10001 11110", "L": "10000 10000 10000 10000 10000 10000 11111",
 "G": "01110 10001 10000 10111 10001 10001 01111", "I": "01110 00100 00100 00100 00100 00100 01110",
 "K": "10001 10010 10100 11000 10100 10010 10001",
 "A": "01110 10001 10001 11111 10001 10001 10001", "Y": "10001 10001 01010 00100 00100 00100 00100",
 "M": "10001 11011 10101 10101 10001 10001 10001",
 "V": "10001 10001 10001 10001 01010 01010 00100",
}

def chunk(t, d):
    return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

def png(path, pixels, w, h, rgba=False):
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6 if rgba else 2, 0, 0, 0))
                           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))

def face(x, y):
    v = math.sin(x * 0.33 + y * 0.21) + math.sin(y * 0.47 - x * 0.13) + math.sin((x + y) * 0.11 + 1.3)
    t = max(0.0, min(0.999, 0.55 + v / 6 * 0.45 + (0.22 - y / H * 0.5)))
    level = t * 4
    base = int(level)
    idx = base + (1 if level - base > (BAYER[y % 4][x % 4] + 0.5) / 16 else 0)
    return FACE[max(0, min(3, idx))]

def bevel(x, y):
    d_top, d_left, d_bot, d_right = y, x, H - 1 - y, W - 1 - x
    m = min(d_top, d_left, d_bot, d_right)
    if m >= 4:
        return None
    if m == d_top:
        return BEV_TOP[0 if d_top < 2 else 1]
    if m == d_left:
        return BEV_LEFT[0 if d_left < 2 else 1]
    if m == d_bot:
        return BEV_BOTTOM[0 if d_bot < 2 else 1]
    return BEV_RIGHT[0 if d_right < 2 else 1]

def shape_news(s):
    s.update((x, y) for y in range(6, 25) for x in range(28, 35))
    s.update((x, y) for y in range(28, 34) for x in range(28, 35))

def shape_projects(s):
    cx, cy = 31, 19
    for y in range(cy - 12, cy + 13):
        for x in range(cx - 12, cx + 13):
            d = math.hypot(x - cx, y - cy)
            if 7.5 <= d <= 12 or d <= 3.2:
                s.add((x, y))

def shape_blog(s):
    for y in range(6, 33):
        for x in range(21, 42):
            if x < 24 or x > 38 or y < 9 or y > 29 or (x in range(25, 38) and y in (13, 14, 19, 20, 25, 26)):
                s.add((x, y))

def shape_links(s):
    cx, cy = 31, 19
    for y in range(cy - 13, cy + 14):
        for x in range(cx - 13, cx + 14):
            d = math.hypot(x - cx, y - cy)
            meridian = abs(x - cx) <= 1 or (abs(((x - cx) / 6.5) ** 2 + ((y - cy) / 12) ** 2 - 1) < 0.28 and d < 12.5)
            if 10 <= d <= 12.5 or meridian or (abs(y - cy) <= 1 and d < 12.5):
                s.add((x, y))

def shape_library(s):
    # a stack of three books seen from the side
    for (y0, x0, x1) in ((8, 20, 42), (16, 22, 43), (24, 19, 41)):
        for y in range(y0, y0 + 6):
            for x in range(x0, x1):
                if y in (y0, y0 + 5) or x in (x0, x1 - 1) or x in (x0 + 3, x0 + 4):
                    s.add((x, y))

def shape_games(s):
    # a game controller: rounded body, d-pad on the left, two buttons on the right
    x0, x1, y0, y1, r = 13, 49, 9, 31, 7
    def inside(x, y, k=0):
        cx = min(max(x, x0 + r - k), x1 - r + k)
        cy = min(max(y, y0 + r - k), y1 - r + k)
        return x0 + k <= x <= x1 - k and y0 + k <= y <= y1 - k and math.hypot(x - cx, y - cy) <= r - k + 0.5
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if inside(x, y) and not inside(x, y, 3):
                s.add((x, y))
    for y in range(17, 24):
        for x in range(19, 26):
            if (y in (19, 20, 21)) or (x in (21, 22, 23)):
                s.add((x, y))
    for (cx, cy) in ((38, 18), (43, 22)):
        for y in range(cy - 2, cy + 3):
            for x in range(cx - 2, cx + 3):
                if math.hypot(x - cx, y - cy) <= 2.2:
                    s.add((x, y))

def shape_inventory(s):
    # a PC tower: case, two drive slots, a power button
    for y in range(5, 33):
        for x in range(23, 40):
            if x in (23, 24, 38, 39) or y in (5, 6, 31, 32) or (y in (11, 12, 15, 16) and 27 <= x <= 36):
                s.add((x, y))
    cx, cy = 31, 25
    for y in range(cy - 2, cy + 3):
        for x in range(cx - 2, cx + 3):
            if math.hypot(x - cx, y - cy) <= 2.4:
                s.add((x, y))

def draw_label(img, text):
    x0, y0 = (W - (len(text) * 6 - 1)) // 2, 40
    on = set()
    for i, ch in enumerate(text):
        for ry, row in enumerate(FONT[ch].split()):
            for rx, bit in enumerate(row):
                if bit == "1":
                    on.add((x0 + i * 6 + rx, y0 + ry))
    for (x, y) in on:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)):
            p = (x + dx, y + dy)
            if p not in on and 4 <= p[0] < W - 4 and 4 <= p[1] < H - 4:
                img[p[1]][p[0]] = OUTLINE
    for (x, y) in on:
        img[y][x] = WHITE

def button(key, label, shape):
    img = [[bevel(x, y) or face(x, y) for x in range(W)] for y in range(H)]
    s = set()
    shape(s)
    inside = lambda p: 4 <= p[0] < W - 4 and 4 <= p[1] < 38
    for (x, y) in s:
        p = (x + 1, y + 1)
        if p not in s and inside(p):
            img[p[1]][p[0]] = ICON_DARK
    for (x, y) in s:
        if inside((x, y)):
            img[y][x] = ICON_MAIN
    for (x, y) in s:
        if inside((x, y)) and ((x - 1, y) not in s or (x, y - 1) not in s):
            img[y][x] = ICON_LIGHT
    draw_label(img, label)
    png(os.path.join(OUT, "btn-%s.png" % key), img, W, H)

def arrow():
    aw, ah = 32, 24
    img = [[(0, 0, 0, 0)] * aw for _ in range(ah)]
    cy, tip = 11.5, 31.0
    for y in range(ah):
        for x in range(aw):
            half = (ah / 2 - 1) * (1 - x / tip)
            if abs(y - cy) <= half + 0.5 and not (x < 3 and abs(y - cy) < 2):
                t = (y - (cy - half)) / max(1.0, 2 * half)
                c = (255, 150, 170) if t < 0.28 else (226, 38, 60) if t < 0.55 else (178, 24, 44) if t < 0.8 else (116, 19, 32)
                img[y][x] = c + (255,)
    edge = [[False] * aw for _ in range(ah)]
    for y in range(ah):
        for x in range(aw):
            if img[y][x][3]:
                nb = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                if any(not (0 <= a < aw and 0 <= b < ah) or not img[b][a][3] for a, b in nb):
                    edge[y][x] = True
    for y in range(ah):
        for x in range(aw):
            if edge[y][x]:
                img[y][x] = (58, 15, 20, 255)
    for x in range(5, 17):
        y = 5 + (x - 5) // 3
        if img[y][x][3]:
            img[y][x] = (255, 214, 224, 255)
    png(os.path.join(OUT, "arrow.png"), img, aw, ah, rgba=True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    button("news", "NEWS", shape_news)
    button("projects", "PROJECTS", shape_projects)
    button("library", "LIBRARY", shape_library)
    button("inventory", "INVENTORY", shape_inventory)
    button("games", "GAMES", shape_games)
    arrow()
    print("ok")
