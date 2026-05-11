from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "pet" / "spritesheet.png"
OUT = ROOT / "assets" / "wallpapers"


def extract_first_frame(strip: Image.Image) -> Image.Image:
    frame = strip.crop((0, 0, 192, 208)).convert("RGBA")
    return frame.crop(frame.getchannel("A").getbbox())


def extract_idle_frames() -> list[Image.Image]:
    strip = Image.open(SOURCE).convert("RGBA")
    frames = []
    for index in range(6):
        frame = strip.crop((index * 192, 0, (index + 1) * 192, 208))
        frames.append(frame.crop(frame.getchannel("A").getbbox()))
    return frames


def paste_pixel(base: Image.Image, sprite: Image.Image, center: tuple[int, int], scale: float) -> None:
    size = (int(sprite.width * scale), int(sprite.height * scale))
    scaled = sprite.resize(size, Image.Resampling.NEAREST)
    base.alpha_composite(scaled, (int(center[0] - size[0] / 2), int(center[1] - size[1] / 2)))


def paw(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, fill: tuple[int, int, int, int]) -> None:
    draw.ellipse((x, y + s * 0.7, x + s * 1.4, y + s * 2.1), fill=fill)
    draw.ellipse((x - s * 0.7, y, x + s * 0.1, y + s * 0.8), fill=fill)
    draw.ellipse((x + s * 0.3, y - s * 0.25, x + s * 1.1, y + s * 0.55), fill=fill)
    draw.ellipse((x + s * 1.3, y, x + s * 2.1, y + s * 0.8), fill=fill)


def sparkle(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, fill: tuple[int, int, int, int]) -> None:
    draw.polygon(
        [
            (x, y - s),
            (x + s * 0.22, y - s * 0.22),
            (x + s, y),
            (x + s * 0.22, y + s * 0.22),
            (x, y + s),
            (x - s * 0.22, y + s * 0.22),
            (x - s, y),
            (x - s * 0.22, y - s * 0.22),
        ],
        fill=fill,
    )


def make_wallpaper(name: str, size: tuple[int, int], center: tuple[int, int], scale: float, pattern: str) -> None:
    pet = extract_first_frame(Image.open(SOURCE))
    img = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    cream = (248, 220, 145, 42)
    peach = (255, 170, 150, 32)
    gold = (246, 198, 115, 28)

    if pattern == "desktop":
        for i, (x, y) in enumerate([(260, 280), (650, 1660), (1160, 520), (2140, 320), (3090, 600), (3420, 1660), (2480, 1840)]):
            paw(draw, x, y, 26 + (i % 2) * 8, cream)
        for x, y, s in [(520, 840, 18), (930, 250, 14), (2860, 260, 18), (3260, 1090, 16), (1960, 1540, 13)]:
            sparkle(draw, x, y, s, peach)
    elif pattern == "phone":
        for i, (x, y) in enumerate([(120, 360), (1040, 520), (210, 1180), (1130, 1500), (170, 2420), (1050, 2700)]):
            paw(draw, x, y, 20 + (i % 2) * 5, cream)
        for x, y, s in [(720, 410, 15), (320, 1780, 12), (1020, 2190, 14), (680, 2860, 10)]:
            sparkle(draw, x, y, s, gold)
    elif pattern == "watch":
        for x, y, s in [(55, 70, 5), (335, 92, 6), (72, 410, 5), (340, 386, 5)]:
            sparkle(draw, x, y, s, peach)
    else:
        for i, (x, y) in enumerate([(120, 280), (850, 360), (160, 900), (880, 1220), (190, 1640)]):
            paw(draw, x, y, 17 + (i % 2) * 4, cream)
        for x, y, s in [(520, 250, 12), (770, 760, 10), (330, 1380, 11), (760, 1720, 10)]:
            sparkle(draw, x, y, s, peach)

    paste_pixel(img, pet, center, scale)
    OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT / name, quality=95)


def soft_background(size: tuple[int, int], pattern: str) -> Image.Image:
    img = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(img, "RGBA")
    cream = (248, 220, 145, 36)
    peach = (255, 170, 150, 30)
    gold = (246, 198, 115, 26)
    w, h = size

    if pattern == "desktop-sequence":
        for i, x in enumerate([260, 850, 1450, 2100, 2720, 3360]):
            paw(draw, x, 320 if i % 2 else 1690, 24, cream)
        for x, y, s in [(500, 900, 14), (1220, 520, 12), (2320, 470, 15), (3220, 1060, 13)]:
            sparkle(draw, x, y, s, peach)
    elif pattern == "phone-sequence":
        for i, (x, y) in enumerate([(150, 350), (1080, 650), (180, 1280), (1060, 1820), (230, 2460), (1110, 2910)]):
            paw(draw, x, y, 18 + (i % 2) * 4, cream)
        for x, y, s in [(710, 260, 12), (380, 920, 9), (1010, 1490, 11), (400, 2220, 9), (760, 2980, 10)]:
            sparkle(draw, x, y, s, gold)
    elif pattern == "watch-sequence":
        for x, y, s in [(55, 58, 4), (350, 68, 5), (54, h - 72, 4), (350, h - 62, 5)]:
            sparkle(draw, x, y, s, peach)
    else:
        for i, (x, y) in enumerate([(120, 280), (910, 380), (150, 1020), (900, 1510)]):
            paw(draw, x, y, 15 + (i % 2) * 3, cream)
        for x, y, s in [(520, 250, 10), (770, 760, 9), (330, 1380, 10), (760, 1740, 8)]:
            sparkle(draw, x, y, s, peach)
    return img


def make_sequence_wallpaper(name: str, size: tuple[int, int], layout: str) -> None:
    frames = extract_idle_frames()
    img = soft_background(size, layout)
    w, h = size

    if layout == "desktop-sequence":
        centers = [(520, 1120), (1080, 1120), (1640, 1120), (2200, 1120), (2760, 1120), (3320, 1120)]
        scale = 2.35
    elif layout == "phone-sequence":
        centers = [(w // 2, y) for y in [420, 900, 1380, 1860, 2340, 2820]]
        scale = 2.35
    elif layout == "wechat-sequence":
        centers = [(310, 470), (770, 470), (310, 970), (770, 970), (310, 1470), (770, 1470)]
        scale = 1.65
    elif layout == "watch-sequence":
        centers = [
            (int(w * 0.30), int(h * 0.26)),
            (int(w * 0.70), int(h * 0.26)),
            (int(w * 0.30), int(h * 0.50)),
            (int(w * 0.70), int(h * 0.50)),
            (int(w * 0.30), int(h * 0.74)),
            (int(w * 0.70), int(h * 0.74)),
        ]
        scale = min(w / 500, h / 610)
    else:
        raise ValueError(f"unknown layout: {layout}")

    for frame, center in zip(frames, centers):
        paste_pixel(img, frame, center, scale)

    OUT.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(OUT / name, quality=95)


def paste_thumbnail(base: Image.Image, path: Path, box: tuple[int, int, int, int]) -> None:
    thumb = Image.open(path).convert("RGB")
    thumb.thumbnail((box[2] - box[0], box[3] - box[1]), Image.Resampling.LANCZOS)
    x = box[0] + (box[2] - box[0] - thumb.width) // 2
    y = box[1] + (box[3] - box[1] - thumb.height) // 2
    base.paste(thumb, (x, y))


def make_sequence_preview() -> None:
    img = Image.new("RGB", (1800, 1200), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    ink = (116, 83, 55)
    faint = (244, 230, 190)

    draw.text((64, 48), "Mimi six-frame idle sequence wallpapers", fill=ink)
    panels = [
        ("Desktop sequence", "mimi-idle-sequence-desktop-3840x2160-white.png", (60, 110, 910, 590)),
        ("Phone sequence", "mimi-idle-sequence-phone-1440x3200-white.png", (1020, 110, 1320, 770)),
        ("WeChat sequence", "mimi-idle-sequence-wechat-1080x1920-white.png", (1370, 110, 1670, 650)),
        ("Watch sequence", "mimi-idle-sequence-watch-410x502-white.png", (1040, 840, 1220, 1060)),
        ("Watch 396 sequence", "mimi-idle-sequence-watch-396x484-white.png", (1340, 840, 1520, 1060)),
    ]

    for label, filename, box in panels:
        draw.rounded_rectangle(box, radius=8, outline=faint, width=3)
        draw.text((box[0], box[1] - 28), label, fill=ink)
        paste_thumbnail(img, OUT / filename, (box[0] + 10, box[1] + 10, box[2] - 10, box[3] - 10))

    img.save(OUT / "mimi-idle-sequence-preview.png", quality=95)


def main() -> None:
    make_wallpaper("mimi-desktop-3840x2160-white.png", (3840, 2160), (2900, 1240), 5.3, "desktop")
    make_wallpaper("mimi-phone-1440x3200-white.png", (1440, 3200), (720, 1820), 4.8, "phone")
    make_wallpaper("mimi-wechat-1080x1920-white.png", (1080, 1920), (540, 1120), 3.7, "wechat")
    make_wallpaper("mimi-watch-410x502-white.png", (410, 502), (205, 270), 1.65, "watch")
    make_wallpaper("mimi-watch-396x484-white.png", (396, 484), (198, 260), 1.58, "watch")
    make_sequence_wallpaper("mimi-idle-sequence-desktop-3840x2160-white.png", (3840, 2160), "desktop-sequence")
    make_sequence_wallpaper("mimi-idle-sequence-phone-1440x3200-white.png", (1440, 3200), "phone-sequence")
    make_sequence_wallpaper("mimi-idle-sequence-wechat-1080x1920-white.png", (1080, 1920), "wechat-sequence")
    make_sequence_wallpaper("mimi-idle-sequence-watch-410x502-white.png", (410, 502), "watch-sequence")
    make_sequence_wallpaper("mimi-idle-sequence-watch-396x484-white.png", (396, 484), "watch-sequence")
    make_sequence_preview()


if __name__ == "__main__":
    main()
