from __future__ import annotations

from html import escape
from pathlib import Path

from captured_proof_demo import DEMO_FRAME_DURATIONS_MS, DemoResult, run_demo
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
GIF_PATH = ASSET_DIR / "doneproof-demo.gif"
SVG_PATH = ASSET_DIR / "doneproof-demo.svg"
POSTER_PATH = ASSET_DIR / "doneproof-demo-poster.png"
SOCIAL_PREVIEW_PATH = ASSET_DIR / "doneproof-social-preview.png"

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


def load_display_font(size: int) -> ImageFont.FreeTypeFont:
    for candidate in (
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return load_font(size)


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


def _short_digest(value: object) -> str:
    text = str(value)
    if text.startswith("sha256:"):
        return f"sha256:{text[7:23]}…"
    return text


def build_frames(result: DemoResult) -> list[Image.Image]:
    proof = result.receipt["captured_proof"]
    output = proof["output"]
    git_scope = proof["git_scope"]
    return [
        render_frame(
            "Local check evidence for AI code changes",
            [
                ("Run the check.", "accent"),
                ("Get a shareable receipt tied to the current Git change.", "accent"),
                ("", "muted"),
                ("$ doneproof capture --task \"Check this change\" -- \\", "prompt"),
                ("    git diff --check", "prompt"),
                ("", "muted"),
                ("Evidence first. Human review remains final.", "ok"),
            ],
        ),
        render_frame(
            "One real command. One current change.",
            [
                ("Changed file auto-selected: README.md", "accent"),
                ("Running: git diff --check", "prompt"),
                ("", "muted"),
                (
                    f"Captured Proof: PASS  ·  exit 0  ·  {proof['duration_ms']} ms",
                    "ok",
                ),
                ("Receipt: .doneproof/receipts/latest.json", "muted"),
                ("Review state: awaiting_review", "warn"),
                ("The CLI recorded the run; nobody typed “passed”.", "accent"),
            ],
        ),
        render_frame(
            "Evidence without storing the evidence payload",
            [
                (f"output       {_short_digest(output['sha256'])}", "muted"),
                (f"git scope     {_short_digest(git_scope['sha256'])}", "muted"),
                (f"integrity     {_short_digest(proof['integrity_sha256'])}", "muted"),
                ("raw output     not stored", "ok"),
                ("Git diff       not stored", "ok"),
                ("changed file   README.md", "accent"),
                ("", "muted"),
                ("The receipt is tied to this Git change.", "accent"),
            ],
        ),
        render_frame(
            "Share the receipt. Keep human review.",
            [
                ("$ doneproof check", "prompt"),
                ("Check result: PASS", "ok"),
                ("$ doneproof schema-check", "prompt"),
                ("DoneProof schema: PASS", "ok"),
                ("$ doneproof report", "prompt"),
                ("Task: Check this change", "ok"),
                ("Receipt status: awaiting_review", "warn"),
                (f"Full demo runtime: {result.elapsed_seconds:.2f} seconds", "muted"),
                ("Machine-captured receipt → human review", "accent"),
            ],
        ),
    ]


def write_svg(result: DemoResult) -> None:
    proof = result.receipt["captured_proof"]
    output = proof["output"]
    git_scope = proof["git_scope"]
    lines = [
        ("$ doneproof capture --task \"Check this change\" -- git diff --check", TEXT),
        ("Changed file auto-selected: README.md", CYAN),
        (f"exit 0 · {proof['duration_ms']} ms · raw output not stored", GREEN),
        (f"output    {_short_digest(output['sha256'])}", MUTED),
        (f"git scope  {_short_digest(git_scope['sha256'])}", MUTED),
        (f"integrity  {_short_digest(proof['integrity_sha256'])}", MUTED),
        ("check: PASS · schema: PASS · report: PASS", GREEN),
        (f"Real isolated demo: {result.elapsed_seconds:.2f}s", CYAN),
        ("Shareable receipt → human review remains final.", TEXT),
    ]
    text = "\n".join(
        (
            f'  <text x="70" y="{132 + index * 44}" '
            f'fill="{color}" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            f'font-size="24">{escape(line)}</text>'
        )
        for index, (line, color) in enumerate(lines)
    )
    SVG_PATH.write_text(
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
            'aria-label="Captured Proof demonstration">\n'
            f'  <rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}"/>\n'
            '  <rect x="32" y="30" width="1036" height="560" rx="14" '
            f'fill="{WINDOW}" stroke="{BORDER}"/>\n'
            '  <rect x="32" y="30" width="1036" height="54" rx="14" '
            f'fill="{HEADER}"/>\n'
            f'  <text x="550" y="64" text-anchor="middle" fill="{TEXT}" '
            'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
            'font-size="19">Captured Proof v0.6 candidate</text>\n'
            f"{text}\n"
            "</svg>\n"
        ),
        encoding="utf-8",
    )


def write_social_preview(result: DemoResult) -> None:
    proof = result.receipt["captured_proof"]
    width = 1280
    height = 640
    image = Image.new("RGB", (width, height), "#0b0e12")
    draw = ImageDraw.Draw(image)

    display_large = load_display_font(72)
    display_medium = load_display_font(34)
    display_small = load_display_font(21)
    mono = load_font(22)
    mono_small = load_font(19)

    draw.rounded_rectangle(
        (28, 28, width - 28, height - 28),
        radius=24,
        fill="#10151b",
        outline="#26313b",
        width=2,
    )
    draw.text(
        (76, 74),
        "UNRELEASED CANDIDATE  ·  LOCAL CHECK EVIDENCE",
        fill="#83d6ff",
        font=display_small,
    )
    draw.text((72, 135), "Captured Proof", fill="#f7f9fb", font=display_large)
    draw.text(
        (76, 228),
        "See what actually ran.",
        fill="#aeb8c2",
        font=display_medium,
    )
    draw.text(
        (76, 302),
        "One observed command.",
        fill="#e8edf2",
        font=display_small,
    )
    draw.text(
        (76, 338),
        "One current Git change.",
        fill="#e8edf2",
        font=display_small,
    )
    draw.text(
        (76, 374),
        "One reviewable receipt.",
        fill="#e8edf2",
        font=display_small,
    )

    card = (650, 82, 1204, 480)
    draw.rounded_rectangle(card, radius=18, fill="#090c0f", outline="#2e3944", width=2)
    draw.rounded_rectangle(
        (650, 82, 1204, 132),
        radius=18,
        fill="#171d23",
    )
    draw.rectangle((650, 114, 1204, 132), fill="#171d23")
    draw.text((680, 96), "REAL RECEIPT", fill="#97a4b1", font=mono_small)

    terminal_lines = [
        ('$ doneproof capture --task "Check', "#f5f7fa"),
        ('  this change" -- git diff --check', "#f5f7fa"),
        ("", "#f5f7fa"),
        (f"✓ exit 0  ·  {proof['duration_ms']} ms", "#7adf9b"),
        ("git scope   1 changed file", "#83d6ff"),
        ("raw output  not stored", "#7adf9b"),
        ("review      awaiting_review", "#ffd479"),
    ]
    y = 158
    for line, color in terminal_lines:
        draw.text((680, y), line, fill=color, font=mono)
        y += 40

    flow_y = 532
    flow = [
        ("COMMAND", 76, 264),
        ("GIT SCOPE", 346, 570),
        ("REVIEWABLE RECEIPT", 664, 1054),
    ]
    for label, left, right in flow:
        draw.rounded_rectangle(
            (left, flow_y, right, flow_y + 54),
            radius=27,
            fill="#18212a",
            outline="#334454",
        )
        draw.text(
            ((left + right) / 2, flow_y + 27),
            label,
            fill="#eaf0f5",
            anchor="mm",
            font=mono_small,
        )
    draw.text((305, flow_y + 27), "→", fill="#83d6ff", anchor="mm", font=mono)
    draw.text((617, flow_y + 27), "→", fill="#83d6ff", anchor="mm", font=mono)

    image.save(SOCIAL_PREVIEW_PATH, optimize=True)


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    result = run_demo()
    frames = build_frames(result)
    frames[0].save(
        GIF_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=DEMO_FRAME_DURATIONS_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    frames[-1].save(POSTER_PATH, optimize=True)
    write_svg(result)
    write_social_preview(result)
    print(f"wrote {GIF_PATH.relative_to(ROOT)}")
    print(f"wrote {POSTER_PATH.relative_to(ROOT)}")
    print(f"wrote {SVG_PATH.relative_to(ROOT)}")
    print(f"wrote {SOCIAL_PREVIEW_PATH.relative_to(ROOT)}")
    print(f"demo runtime: {result.elapsed_seconds:.2f}s")
    print(f"animation runtime: {sum(DEMO_FRAME_DURATIONS_MS) / 1000:.1f}s")


if __name__ == "__main__":
    main()
