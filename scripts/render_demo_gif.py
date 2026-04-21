from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
GIF_PATH = ASSET_DIR / "doneproof-demo.gif"
SVG_PATH = ASSET_DIR / "doneproof-demo.svg"
POSTER_PATH = ASSET_DIR / "doneproof-demo-poster.png"

WIDTH = 1100
HEIGHT = 620
PADDING_X = 70
HEADER_HEIGHT = 54
BODY_TOP = 112
LINE_HEIGHT = 34

BACKGROUND = "#f4f4ef"
WINDOW = "#111315"
HEADER = "#1d2126"
BORDER = "#2a2f35"
TEXT = "#f5f7fa"
MUTED = "#9aa4af"
GREEN = "#7adf9b"
RED = "#ff8f8f"
AMBER = "#ffd479"
CYAN = "#83d6ff"


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in (
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Menlo.ttc",
    ):
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT = load_font(24)
FONT_BOLD = load_font(26)
FONT_SMALL = load_font(19)


def draw_window(draw: ImageDraw.ImageDraw, title: str) -> None:
    draw.rounded_rectangle(
        (32, 30, WIDTH - 32, HEIGHT - 30),
        radius=14,
        fill=WINDOW,
        outline=BORDER,
    )
    draw.rounded_rectangle((32, 30, WIDTH - 32, 30 + HEADER_HEIGHT), radius=14, fill=HEADER)
    draw.rectangle((32, 30 + HEADER_HEIGHT - 14, WIDTH - 32, 30 + HEADER_HEIGHT), fill=HEADER)
    for i, color in enumerate(("#ff6359", "#ffbd3f", "#27c93f")):
        cx = 58 + i * 20
        cy = 58
        draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=color)
    draw.text((WIDTH / 2, 50), title, fill=TEXT, anchor="mm", font=FONT_SMALL)


def draw_lines(draw: ImageDraw.ImageDraw, lines: list[tuple[str, str]]) -> None:
    y = BODY_TOP
    for text, style in lines:
        color = {
            "prompt": TEXT,
            "ok": GREEN,
            "error": RED,
            "muted": MUTED,
            "accent": CYAN,
            "warn": AMBER,
        }[style]
        font = FONT_BOLD if style in {"ok", "error"} else FONT
        draw.text((PADDING_X, y), text, fill=color, font=font)
        y += LINE_HEIGHT


def render_frame(title: str, lines: list[tuple[str, str]]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw_window(draw, title)
    draw_lines(draw, lines)
    return image


def build_frames() -> list[Image.Image]:
    return [
        render_frame(
            "doneproof init",
            [
                ("$ doneproof init", "prompt"),
                ("DoneProof initialized at .", "ok"),
                ("created: .doneproof/policy.yml", "muted"),
                ("created: .doneproof/templates/codex.md", "muted"),
                ("created: .doneproof/receipts/.gitkeep", "muted"),
                ("", "muted"),
                ("Agents now have a receipt policy to follow.", "accent"),
            ],
        ),
        render_frame(
            "doneproof evidence git-diff",
            [
                ("$ doneproof evidence git-diff", "prompt"),
                ("created: .doneproof/evidence/git-diff-summary.txt", "ok"),
                ("safe summary: files + addition/deletion counts", "muted"),
                ("full diff content is intentionally omitted", "warn"),
                ("", "muted"),
                ("Reviewers get shape without turning receipts into a secret sink.", "accent"),
            ],
        ),
        render_frame(
            "doneproof check",
            [
                ("$ doneproof check --receipt examples/receipts/failing.json", "prompt"),
                ("DoneProof: FAIL", "error"),
                ("error: Forbidden status: done", "error"),
                ("error: changed_files needs at least 1 item(s)", "error"),
                ("error: commands needs at least 1 item(s)", "error"),
                ("error: evidence needs at least 1 item(s)", "error"),
            ],
        ),
        render_frame(
            "doneproof check",
            [
                ("$ doneproof check --receipt examples/receipts/passing.json", "prompt"),
                ("DoneProof: PASS", "ok"),
                ("receipt includes changed files, commands, evidence, and risks", "muted"),
                ("No proof, no done.", "accent"),
            ],
        ),
        render_frame(
            "doneproof report",
            [
                ("$ doneproof report --receipt examples/receipts/passing.json", "prompt"),
                ("Task: Add a health check endpoint", "muted"),
                ("Status: awaiting_review", "ok"),
                ("Commands: [passed] pytest tests/test_receipt.py", "muted"),
                ("Evidence: test: pytest tests/test_receipt.py passed", "muted"),
                ("Risks: Manual browser check not performed", "warn"),
            ],
        ),
    ]


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    frames = build_frames()
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=[900, 1100, 1400, 1200, 1500],
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"wrote {GIF_PATH.relative_to(ROOT)}")
    if not SVG_PATH.exists():
        raise SystemExit(f"missing static fallback: {SVG_PATH}")


if __name__ == "__main__":
    main()
