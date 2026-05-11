from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "animation-rows" / "idle.png"
OUT = ROOT / "assets" / "wallpapers"


def extract_first_frame(strip: Image.Image) -> Image.Image:
    frame = strip.crop((0, 0, 192, 208)).convert("RGBA")
    return frame.crop(frame.getchannel("A").getbbox())


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


def main() -> None:
    make_wallpaper("mimi-desktop-3840x2160-white.png", (3840, 2160), (2900, 1240), 5.3, "desktop")
    make_wallpaper("mimi-phone-1440x3200-white.png", (1440, 3200), (720, 1820), 4.8, "phone")
    make_wallpaper("mimi-wechat-1080x1920-white.png", (1080, 1920), (540, 1120), 3.7, "wechat")
    make_wallpaper("mimi-watch-410x502-white.png", (410, 502), (205, 270), 1.65, "watch")
    make_wallpaper("mimi-watch-396x484-white.png", (396, 484), (198, 260), 1.58, "watch")


if __name__ == "__main__":
    main()

