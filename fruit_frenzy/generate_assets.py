"""generate_assets.py - Creates every image (PNG) and sound (WAV) in the assets/ folder.

Run once:  python generate_assets.py   (needs Pillow: pip install pillow)
You can later replace any file in assets/ with your own artwork or sounds
(keep the same file names).
"""
import math
import os
import random
import struct
import wave

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "assets", "images")
SND = os.path.join(BASE, "assets", "sounds")
os.makedirs(IMG, exist_ok=True)
os.makedirs(SND, exist_ok=True)

S = 4  # supersampling factor for smooth edges


def canvas(w, h):
    return Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))


def save(img, name, size):
    img.resize(size, Image.LANCZOS).save(os.path.join(IMG, name))


def sc(*vals):
    return [v * S for v in vals]


# ------------------------------------------------------------------ images
def make_apple():
    im = canvas(64, 64); d = ImageDraw.Draw(im)
    d.ellipse(sc(8, 14, 56, 60), fill=(215, 45, 45), outline=(150, 20, 20), width=S)
    d.ellipse(sc(16, 22, 28, 34), fill=(245, 120, 120))
    d.line(sc(32, 16, 34, 6), fill=(110, 70, 30), width=3 * S)
    d.ellipse(sc(34, 4, 52, 16), fill=(70, 170, 70), outline=(40, 110, 40), width=S)
    save(im, "apple.png", (64, 64))


def make_orange():
    im = canvas(64, 64); d = ImageDraw.Draw(im)
    d.ellipse(sc(7, 10, 57, 60), fill=(250, 150, 30), outline=(190, 100, 10), width=S)
    d.ellipse(sc(15, 18, 27, 30), fill=(255, 195, 110))
    for x, y in [(30, 32), (40, 40), (24, 44), (42, 24), (34, 50)]:
        d.ellipse(sc(x, y, x + 2, y + 2), fill=(205, 110, 15))
    d.ellipse(sc(28, 6, 44, 16), fill=(70, 170, 70), outline=(40, 110, 40), width=S)
    save(im, "orange.png", (64, 64))


def make_banana():
    im = canvas(64, 64); d = ImageDraw.Draw(im)
    d.ellipse(sc(4, 4, 62, 62), fill=(250, 220, 60), outline=(180, 140, 20), width=S)
    d.ellipse(sc(16, -10, 76, 48), fill=(0, 0, 0, 0))  # cut out the inside -> crescent
    d.ellipse(sc(8, 10, 16, 18), fill=(110, 75, 30))
    d.ellipse(sc(50, 44, 58, 52), fill=(110, 75, 30))
    save(im, "banana.png", (64, 64))


def make_bomb():
    im = canvas(64, 64); d = ImageDraw.Draw(im)
    d.ellipse(sc(8, 16, 56, 62), fill=(40, 40, 48), outline=(15, 15, 20), width=S)
    d.ellipse(sc(16, 24, 26, 34), fill=(110, 110, 125))
    d.rectangle(sc(26, 8, 38, 18), fill=(120, 120, 130), outline=(60, 60, 70), width=S)
    d.line(sc(32, 8, 40, 2, 46, 4), fill=(170, 120, 60), width=2 * S)
    d.polygon([(S * x, S * y) for x, y in [(46, 0), (49, 4), (54, 4), (50, 7), (52, 12), (46, 9), (41, 12), (43, 7), (39, 4), (44, 4)]],
              fill=(255, 210, 50))
    save(im, "bomb.png", (64, 64))


def make_heart():
    im = canvas(64, 64); d = ImageDraw.Draw(im)
    red, edge = (235, 50, 90), (160, 20, 55)
    d.ellipse(sc(6, 10, 34, 38), fill=red, outline=edge, width=S)
    d.ellipse(sc(30, 10, 58, 38), fill=red, outline=edge, width=S)
    d.polygon([(S * x, S * y) for x, y in [(8, 29), (56, 29), (32, 60)]], fill=red)
    d.ellipse(sc(12, 16, 22, 26), fill=(255, 150, 175))
    save(im, "heart.png", (64, 64))


def make_star():
    im = canvas(64, 64); d = ImageDraw.Draw(im)
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 28 if i % 2 == 0 else 12
        pts.append(((32 + rad * math.cos(ang)) * S, (34 + rad * math.sin(ang)) * S))
    d.polygon(pts, fill=(255, 205, 40), outline=(200, 140, 10))
    d.ellipse(sc(27, 24, 33, 30), fill=(255, 240, 160))
    save(im, "star.png", (64, 64))


def make_basket():
    im = canvas(120, 70); d = ImageDraw.Draw(im)
    d.arc(sc(22, 0, 98, 60), 180, 360, fill=(120, 80, 35), width=5 * S)  # handle
    d.polygon([(S * x, S * y) for x, y in [(4, 22), (116, 22), (102, 66), (18, 66)]],
              fill=(185, 125, 55), outline=(110, 70, 30))
    d.rounded_rectangle(sc(0, 16, 120, 30), radius=6 * S, fill=(150, 95, 40), outline=(100, 62, 25), width=S)
    for x in range(14, 110, 14):  # weave lines
        d.line(sc(x, 32, x - 3 if x < 60 else x + 3, 64), fill=(120, 78, 32), width=2 * S)
    for y in (42, 54):
        d.line(sc(10, y, 110, y), fill=(120, 78, 32), width=2 * S)
    save(im, "basket.png", (120, 70))


def make_background():
    w, h = 800, 600
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):  # sky gradient
        t = y / h
        d.line([(0, y), (w, y)], fill=(int(110 + 100 * t), int(185 + 50 * t), int(245 - 10 * t)))
    d.ellipse((620, 60, 700, 140), fill=(255, 235, 140))  # sun
    random.seed(7)
    for cx, cy in [(120, 110), (330, 70), (520, 150), (700, 230)]:  # clouds
        for dx, dy, r in [(0, 0, 32), (30, 6, 26), (-30, 8, 24), (10, -14, 24)]:
            d.ellipse((cx + dx - r, cy + dy - r * 0.7, cx + dx + r, cy + dy + r * 0.7), fill=(255, 255, 255))
    d.ellipse((-150, 430, 450, 760), fill=(110, 190, 120))  # hills
    d.ellipse((300, 450, 950, 780), fill=(90, 175, 105))
    d.rectangle((0, 540, w, h), fill=(75, 150, 80))
    d.rectangle((0, 540, w, 546), fill=(95, 170, 95))
    im.save(os.path.join(IMG, "background.png"))


# ------------------------------------------------------------------ sounds
RATE = 22050


def write_wav(name, samples):
    with wave.open(os.path.join(SND, name), "w") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE)
        f.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32000)) for s in samples))


def tone(freq, dur, vol=0.5, shape="sine", slide=0.0):
    n = int(RATE * dur); out = []; phase = 0.0
    for i in range(n):
        f = freq + slide * (i / n)
        phase += 2 * math.pi * f / RATE
        v = math.sin(phase) if shape == "sine" else (1.0 if math.sin(phase) >= 0 else -1.0)
        env = min(1.0, i / (RATE * 0.01)) * (1 - i / n) ** 1.5  # quick attack, smooth decay
        out.append(v * vol * env)
    return out


def noise(dur, vol=0.6):
    n = int(RATE * dur)
    return [random.uniform(-1, 1) * vol * (1 - i / n) ** 2 for i in range(n)]


def make_sounds():
    write_wav("catch.wav", tone(660, 0.07) + tone(990, 0.12))
    write_wav("miss.wav", tone(220, 0.25, 0.4, "square", slide=-90))
    bomb = noise(0.45); low = tone(90, 0.45, 0.6, slide=-40)
    write_wav("bomb.wav", [a + b for a, b in zip(bomb, low)])
    write_wav("powerup.wav", tone(523, 0.08) + tone(659, 0.08) + tone(784, 0.08) + tone(1047, 0.2))
    write_wav("win.wav", tone(523, 0.12) + tone(659, 0.12) + tone(784, 0.12) + tone(1047, 0.35))
    write_wav("lose.wav", tone(392, 0.2) + tone(330, 0.2) + tone(262, 0.4, slide=-40))


if __name__ == "__main__":
    for fn in (make_apple, make_orange, make_banana, make_bomb, make_heart, make_star, make_basket, make_background, make_sounds):
        fn()
    print("Assets created in", os.path.join(BASE, "assets"))
