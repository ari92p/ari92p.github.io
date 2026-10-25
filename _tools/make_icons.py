"""Draws the little feature icons for the black bar as 32x32 pixel pictures.

Run:  python3 _tools/make_icons.py
Output: static/img/icons/<name>.png (transparent background). No dependencies.
The CSS shows them at 64x64 with image-rendering: pixelated.
"""
import math, os, struct, zlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "img", "icons")
S = 32
OUTLINE = (20, 32, 44)

BEIGE, BEIGE_D = (216, 208, 176), (172, 164, 132)
GRAY_L, GRAY, GRAY_D = (190, 196, 204), (140, 148, 158), (86, 94, 104)
DARK = (28, 34, 42)
BLUE, BLUE_L, BLUE_D = (64, 130, 214), (120, 180, 240), (24, 60, 130)
GREEN, GREEN_D, GREEN_S = (70, 170, 90), (36, 110, 56), (60, 220, 100)
RED, RED_D = (204, 48, 42), (130, 24, 24)
GOLD, ORANGE = (236, 196, 60), (236, 136, 40)
TEAL, CYAN, WHITE = (44, 160, 170), (110, 220, 235), (246, 246, 240)


class Canvas:
    def __init__(self):
        self.p = {}

    def px(self, x, y, c):
        if 0 <= x < S and 0 <= y < S:
            self.p[(x, y)] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def circle(self, cx, cy, r, c, clip=False):
        for y in range(S):
            for x in range(S):
                if math.hypot(x - cx, y - cy) <= r + 0.3 and (not clip or (x, y) in self.p):
                    self.px(x, y, c)

    def ring(self, cx, cy, r_out, r_in, c):
        for y in range(S):
            for x in range(S):
                d = math.hypot(x - cx, y - cy)
                if r_in <= d <= r_out + 0.3:
                    self.px(x, y, c)

    def ellipse(self, cx, cy, rx, ry, c, r_in=0.0):
        for y in range(S):
            for x in range(S):
                v = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if r_in <= v <= 1.0:
                    self.px(x, y, c)

    def erase_where(self, fn):
        for k in [k for k in self.p if fn(*k)]:
            del self.p[k]

    def line(self, x0, y0, x1, y1, c, t=1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n)
            y = round(y0 + (y1 - y0) * i / n)
            self.rect(x, y, x + t - 1, y + t - 1, c)

    def poly(self, pts, c):
        for y in range(S):
            for x in range(S):
                inside = False
                j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]
                    xj, yj = pts[j]
                    if (yi > y + 0.5) != (yj > y + 0.5) and x + 0.5 < (xj - xi) * (y + 0.5 - yi) / (yj - yi) + xi:
                        inside = not inside
                    j = i
                if inside:
                    self.px(x, y, c)


def lighten(c):
    return tuple(min(255, int(v + (255 - v) * 0.35)) for v in c)


def darken(c):
    return tuple(int(v * 0.68) for v in c)


def write_png(path, canvas):
    pix = canvas.p
    final = {}
    for (x, y), col in pix.items():
        lit = (x - 1, y) not in pix or (x, y - 1) not in pix
        dk = (x + 1, y) not in pix or (x, y + 1) not in pix
        final[(x, y)] = lighten(col) if lit and not dk else darken(col) if dk and not lit else col
    for (x, y) in list(pix):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q not in pix and 0 <= q[0] < S and 0 <= q[1] < S:
                final[q] = OUTLINE
    rows = []
    for y in range(S):
        row = bytearray([0])
        for x in range(S):
            c = final.get((x, y))
            row += bytes(c + (255,)) if c else bytes((0, 0, 0, 0))
        rows.append(bytes(row))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    data = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", S, S, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))
    open(path, "wb").write(data)


def monitor(c, screen, top=3, bottom=22, stand=True):
    c.rect(3, top, 28, bottom, BEIGE)
    c.rect(5, top + 2, 26, bottom - 3, DARK)
    c.rect(6, top + 3, 25, bottom - 4, screen)
    if stand:
        c.rect(12, bottom + 1, 19, bottom + 3, BEIGE_D)
        c.rect(8, bottom + 4, 23, bottom + 6, BEIGE)


def icon_computer(c):
    c.rect(5, 2, 26, 19, BEIGE)
    c.rect(7, 4, 24, 16, DARK)
    c.rect(8, 5, 23, 15, GREEN_D)
    for y in (7, 10, 13):
        c.rect(9, y, 20, y, GREEN_S)
    c.rect(13, 20, 18, 22, BEIGE_D)
    c.rect(4, 24, 27, 29, BEIGE)
    for x in range(6, 26, 2):
        c.px(x, 26, GRAY_D)
        c.px(x, 28, GRAY_D)


def icon_laptop(c):
    c.rect(6, 3, 25, 19, GRAY_D)
    c.rect(8, 5, 23, 17, BLUE)
    c.rect(10, 7, 20, 8, BLUE_L)
    c.rect(10, 11, 16, 12, BLUE_L)
    c.poly([(3, 21), (28, 21), (30, 27), (1, 27)], GRAY_L)
    c.rect(12, 22, 19, 22, GRAY)


def icon_browser(c):
    c.rect(2, 4, 29, 27, WHITE)
    c.rect(2, 4, 29, 9, BLUE)
    for x in (5, 8, 11):
        c.px(x, 6, WHITE)
    c.rect(5, 12, 20, 14, GRAY_L)
    for y in (17, 20, 23):
        c.rect(5, y, 18, y, GRAY)
    c.rect(21, 16, 27, 24, ORANGE)
    c.rect(19, 19, 20, 21, ORANGE)
    c.rect(23, 14, 25, 15, ORANGE)


def icon_globe(c):
    c.circle(15.5, 15.5, 13, BLUE)
    for (cx, cy, r) in ((11, 11, 4), (19, 18, 5), (10, 21, 3), (21, 9, 3)):
        c.circle(cx, cy, r, GREEN, clip=True)
    c.rect(4, 15, 27, 15, BLUE_L)
    for (x, y) in ((9, 6), (10, 5), (11, 5)):
        c.px(x, y, WHITE)


def icon_chip(c):
    c.rect(8, 8, 23, 23, GRAY_D)
    c.rect(11, 11, 20, 20, GRAY)
    c.rect(14, 14, 17, 17, DARK)
    for i in (10, 14, 18, 21):
        c.rect(i, 3, i + 1, 7, GOLD)
        c.rect(i, 24, i + 1, 28, GOLD)
        c.rect(3, i, 7, i + 1, GOLD)
        c.rect(24, i, 28, i + 1, GOLD)


def icon_shield(c):
    c.poly([(5, 4), (26, 4), (26, 16), (15.5, 29), (5, 16)], BLUE)
    c.poly([(8, 7), (23, 7), (23, 15), (15.5, 25), (8, 15)], BLUE_L)
    c.line(10, 15, 14, 20, WHITE, 2)
    c.line(14, 20, 22, 10, WHITE, 2)


def icon_lock(c):
    c.ring(15.5, 12, 8, 5, GRAY_L)
    c.erase_where(lambda x, y: y > 12)
    c.rect(7, 13, 24, 27, GOLD)
    c.circle(15.5, 19, 2, DARK)
    c.rect(15, 19, 16, 23, DARK)


def icon_code(c):
    c.rect(2, 4, 29, 27, DARK)
    c.rect(2, 4, 29, 8, GRAY_D)
    c.line(12, 13, 7, 18, GREEN_S, 2)
    c.line(7, 18, 12, 23, GREEN_S, 2)
    c.line(19, 13, 24, 18, GREEN_S, 2)
    c.line(24, 18, 19, 23, GREEN_S, 2)
    c.line(17, 12, 14, 24, GRAY_L, 1)


def icon_monitorspeaker(c):
    monitor(c, BLUE_D)
    c.rect(9, 10, 11, 14, WHITE)
    c.poly([(11, 9), (15, 6), (15, 18), (11, 15)], WHITE)
    c.ring(15, 12, 7, 5, CYAN)
    c.erase_where(lambda x, y: x < 19 and 5 <= y <= 19 and (x, y) not in [])
    # redraw the speaker after the wave clean-up
    c.rect(9, 10, 11, 14, WHITE)
    c.poly([(11, 9), (15, 6), (15, 18), (11, 15)], WHITE)


def icon_boxes(c):
    for (x0, y0, x1, y1, col) in ((2, 17, 14, 28, BLUE), (17, 17, 29, 28, TEAL), (9, 5, 21, 16, ORANGE)):
        c.rect(x0, y0, x1, y1, col)
        for x in range(x0 + 2, x1, 3):
            c.rect(x, y0 + 2, x, y1 - 2, darken(col))
        c.rect(x0, y0, x1, y0, lighten(col))


def icon_network(c):
    c.line(10, 7, 21, 7, GRAY_D)
    c.line(10, 25, 21, 25, GRAY_D)
    c.line(15, 7, 15, 25, GRAY_D)
    c.line(16, 7, 16, 25, GRAY_D)
    c.rect(12, 14, 19, 18, GRAY_L)
    for (x, y) in ((2, 3), (21, 3), (2, 21), (21, 21)):
        c.rect(x, y, x + 8, y + 6, BEIGE)
        c.rect(x + 1, y + 1, x + 7, y + 4, GREEN)
        c.rect(x + 2, y + 7, x + 6, y + 8, BEIGE_D)


def icon_disk(c):
    c.rect(3, 9, 28, 23, GRAY_L)
    c.rect(5, 12, 26, 20, GRAY_D)
    c.rect(8, 16, 19, 16, DARK)
    c.rect(22, 15, 24, 17, GREEN_S)
    c.rect(3, 9, 28, 10, GRAY)
    for x in (6, 24):
        c.px(x, 22, DARK)


def icon_monitoring(c):
    monitor(c, DARK)
    pts = [(7, 17), (11, 12), (14, 15), (18, 8), (22, 13), (25, 10)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], GREEN_S, 1)
    for x in range(8, 25, 4):
        for y in (10, 14, 18):
            c.px(x, y, GREEN_D)


def icon_book(c):
    c.rect(3, 7, 15, 24, WHITE)
    c.rect(16, 7, 28, 24, WHITE)
    c.rect(15, 7, 15, 24, GRAY)
    for y in (11, 14, 17, 20):
        c.rect(5, y, 13, y, GRAY)
        c.rect(18, y, 26, y, GRAY)
    c.rect(2, 24, 29, 28, RED)


def icon_keyboard(c):
    c.rect(2, 9, 29, 25, GRAY_L)
    for ry in (11, 15, 19):
        for rx in range(4, 27, 4):
            c.rect(rx, ry, rx + 2, ry + 2, WHITE)
    c.rect(8, 22, 22, 23, WHITE)


def icon_license(c):
    c.rect(5, 3, 26, 22, WHITE)
    for y in (7, 10, 13):
        c.rect(8, y, 23, y, GRAY)
    c.rect(12, 22, 14, 29, RED_D)
    c.rect(18, 22, 20, 29, RED_D)
    c.circle(16, 21, 5, RED)
    c.px(16, 21, GOLD)


def icon_layers(c):
    for (cy, col) in ((21, BLUE_D), (15, BLUE), (9, BLUE_L)):
        c.poly([(16, cy - 6), (29, cy), (16, cy + 6), (3, cy)], col)


def icon_eye(c):
    c.ellipse(15.5, 15.5, 13.5, 8.5, WHITE)
    c.circle(15.5, 15.5, 6, BLUE)
    c.circle(15.5, 15.5, 3, DARK)
    c.px(13, 13, WHITE)


def icon_markdown(c):
    c.rect(2, 6, 29, 25, DARK)
    c.line(6, 21, 6, 11, WHITE, 2)
    c.line(6, 11, 10, 16, WHITE, 2)
    c.line(10, 16, 14, 11, WHITE, 2)
    c.line(14, 11, 14, 21, WHITE, 2)
    c.rect(21, 10, 22, 16, WHITE)
    c.poly([(18, 15), (25, 15), (21.5, 21)], WHITE)


ICONS = {
    "computer": icon_computer, "laptop": icon_laptop, "browser": icon_browser, "globe": icon_globe,
    "chip": icon_chip, "shield": icon_shield, "lock": icon_lock, "code": icon_code,
    "monitorspeaker": icon_monitorspeaker, "boxes": icon_boxes, "network": icon_network, "disk": icon_disk,
    "monitoring": icon_monitoring, "book": icon_book, "keyboard": icon_keyboard, "license": icon_license,
    "layers": icon_layers, "eye": icon_eye, "markdown": icon_markdown,
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in ICONS.items():
        c = Canvas()
        fn(c)
        write_png(os.path.join(OUT, name + ".png"), c)
    print("ok", len(ICONS))
