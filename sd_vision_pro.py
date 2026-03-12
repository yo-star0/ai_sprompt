#!/usr/bin/env python3
"""
SD Vision Pro - Stable Diffusion用 画像解析・プロンプト生成ツール
※ Google Gemini API使用（完全無料・クレジットカード不要）

◆ 必要なライブラリのインストール:
    pip install google-generativeai Pillow pyperclip

◆ APIキーの取得（無料・クレジットカード不要）:
    1. https://aistudio.google.com/ にアクセス（Googleアカウントでログイン）
    2. 「Get API key」→「Create API key」でキーを生成
    3. 下記コマンドで環境変数に設定:
       Mac/Linux: export GOOGLE_API_KEY="AIza..."
       Windows:   set GOOGLE_API_KEY=AIza...

◆ 使い方:
    python sd_vision_pro.py image.png
    python sd_vision_pro.py photo.jpg --model realistic
    python sd_vision_pro.py anime.png --model pony
    python sd_vision_pro.py image.png --no-clipboard
"""

import argparse
import sys
from pathlib import Path

# ============================================================
# ライブラリの読み込み（未インストール時は分かりやすいメッセージを表示）
# ============================================================

try:
    import google.generativeai as genai
except ImportError:
    print("=" * 60)
    print("Error: google-generativeai が必要です。")
    print()
    print("以下のコマンドでインストールしてください:")
    print("  pip install google-generativeai")
    print("=" * 60)
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("=" * 60)
    print("Error: Pillow が必要です。")
    print()
    print("以下のコマンドでインストールしてください:")
    print("  pip install Pillow")
    print("=" * 60)
    sys.exit(1)

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


# ============================================================
# 定数
# ============================================================

QUALITY_PREFIX_DEFAULT = "(best quality:1.2), masterpiece, highres"

QUALITY_PREFIX_PONY = "score_9, score_8_up, score_7_up, score_6_up"

NEGATIVE_PROMPT_ANIME = (
    "lowres, bad anatomy, bad hands, text, error, missing fingers, "
    "extra digit, fewer digits, cropped, worst quality, low quality, "
    "normal quality, jpeg artifacts, signature, watermark, username, blurry, "
    "deformed, disfigured, mutation, mutated, ugly, extra limbs, "
    "missing limbs, floating limbs, disconnected limbs, malformed hands, "
    "long neck, long body, 3d, realistic, photo"
)

NEGATIVE_PROMPT_REALISTIC = (
    "illustration, painting, drawing, anime, cartoon, 3d, render, cgi, sketch, "
    "lowres, bad anatomy, bad hands, text, error, missing fingers, "
    "extra digit, fewer digits, cropped, worst quality, low quality, "
    "normal quality, jpeg artifacts, signature, watermark, username, blurry, "
    "deformed, disfigured, mutation, ugly, plastic skin, doll, mannequin, "
    "over-saturated, over-exposed, under-exposed"
)

NEGATIVE_PROMPT_PONY = (
    "score_1, score_2, score_3, score_4, score_5, "
    "lowres, bad anatomy, bad hands, text, error, "
    "missing fingers, extra digit, fewer digits, "
    "cropped, worst quality, low quality, normal quality, "
    "jpeg artifacts, signature, watermark, username, blurry, "
    "deformed, disfigured, mutation, ugly"
)

# Geminiへの指示プロンプト
ANALYSIS_PROMPT = """\
You are a Stable Diffusion prompt expert. Analyze this image and generate \
a precise SD prompt in comma-separated English tag format.

## Output format (strictly follow this):
Line 1: STYLE: anime   (or)   STYLE: realistic
Line 2: (blank)
Line 3: the complete comma-separated tag prompt

## Style detection:
- "anime": anime, illustration, cartoon, manga, digital art, drawing
- "realistic": photograph, photorealistic, real person, 3D render

## Tags to extract (in this order):
1. Subject: gender/count (1girl, 1boy, solo, couple, etc.)
2. Hair: length + style + color (long hair, blonde hair, ponytail, etc.)
3. Eyes: color + style (blue eyes, sparkling eyes, etc.)
4. Expression: emotion (smile, blush, expressionless, etc.)
5. Body: build (slender, petite, curvy, muscular, etc.)
6. Clothing: full description (school uniform, white shirt, pleated skirt, etc.)
7. Accessories: (glasses, choker, hair ribbon, etc.)
8. Pose: body position (standing, sitting, arms crossed, etc.)
9. Composition: framing (upper body, full body, close-up, from above, etc.)
10. Background: setting (classroom, cherry blossoms, night city, etc.)
11. Lighting: type (soft lighting, golden hour, rim lighting, etc.)
12. Effects/atmosphere: (bokeh, depth of field, particles, etc.)
13. Art style specifics:
    - anime: (cel shading, vibrant colors, clean lines, etc.)
    - realistic: (shallow depth of field, 85mm lens, film grain, etc.)

## Weighting rules (use sparingly, only for defining features):
- Most prominent feature: (tag:1.3)
- Clearly visible: (tag:1.2)
- Notable: (tag:1.1)
- Normal: no weight

## Important:
- Use established SD/Danbooru tag conventions
- Be specific: "pleated skirt" not "skirt", "long wavy hair" not "hair"
- Include 20-45 tags total
- Output ONLY the 3 lines above. No explanation, no markdown.
"""


# ============================================================
# 画像読み込み
# ============================================================

SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}


def load_image(image_path: str) -> Image.Image:
    """画像ファイルを読み込んでPIL Imageを返す。"""
    path = Path(image_path)

    if not path.exists():
        print(f"Error: ファイルが見つかりません → {image_path}")
        sys.exit(1)

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        print(f"Error: 非対応の画像形式です → {path.suffix}")
        print(f"  対応形式: {', '.join(sorted(SUPPORTED_FORMATS)).upper()}")
        sys.exit(1)

    try:
        img = Image.open(path)
        img.load()  # 完全に読み込んで破損チェック
        return img
    except Exception as e:
        print(f"Error: 画像の読み込みに失敗しました → {e}")
        sys.exit(1)


# ============================================================
# Gemini APIで画像を解析
# ============================================================

def setup_gemini() -> None:
    """Gemini APIキーを設定する。"""
    import os
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("=" * 60)
        print("Error: GOOGLE_API_KEY が設定されていません。")
        print()
        print("【無料APIキーの取得手順】")
        print("  1. https://aistudio.google.com/ にアクセス")
        print("     （Googleアカウントでログイン、クレジットカード不要）")
        print("  2. 「Get API key」→「Create API key」")
        print("  3. キーをコピーして以下を実行:")
        print()
        print("  Mac/Linux:")
        print('    export GOOGLE_API_KEY="AIza..."')
        print()
        print("  Windows:")
        print("    set GOOGLE_API_KEY=AIza...")
        print("=" * 60)
        sys.exit(1)
    genai.configure(api_key=api_key)


def analyze_image(img: Image.Image) -> tuple[str, str]:
    """Geminiで画像を解析し (style, raw_tags) を返す。"""
    model = genai.GenerativeModel("gemini-2.0-flash")

    print("🔍 画像を解析中...")
    print()

    try:
        response = model.generate_content([ANALYSIS_PROMPT, img])
    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "API key not valid" in error_msg:
            print("Error: APIキーが無効です。Google AI Studioで確認してください。")
            print("  https://aistudio.google.com/")
        elif "QUOTA_EXCEEDED" in error_msg or "quota" in error_msg.lower():
            print("Error: 無料枠の上限に達しました。")
            print("  1日1,500回 / 1分15回が上限です。少し待ってから再試行してください。")
        elif "SAFETY" in error_msg:
            print("Error: この画像はGeminiの安全フィルターによりブロックされました。")
        else:
            print(f"Error: APIリクエストに失敗しました → {e}")
        sys.exit(1)

    response_text = response.text.strip()

    # レスポンスをパース
    lines = [line.strip() for line in response_text.split("\n") if line.strip()]

    style = "anime"
    raw_tags = ""

    for line in lines:
        if line.upper().startswith("STYLE:"):
            value = line.split(":", 1)[1].strip().lower()
            style = "realistic" if ("realistic" in value or "photo" in value) else "anime"
        elif len(line) > len(raw_tags) and not line.upper().startswith("STYLE:"):
            raw_tags = line

    if not raw_tags:
        # フォールバック: 全行を結合
        raw_tags = ", ".join(
            line for line in lines if not line.upper().startswith("STYLE:")
        )

    return style, raw_tags


# ============================================================
# プロンプト構築
# ============================================================

def build_prompt(style: str, raw_tags: str, model_preset: str) -> tuple[str, str]:
    """品質タグ付きの完全なプロンプトとネガティブプロンプトを構築する。"""
    # タグを正規化（余分な空白除去）
    tags = ", ".join(t.strip() for t in raw_tags.split(",") if t.strip())

    # モデル別の品質プレフィックスとネガティブプロンプト
    if model_preset == "pony":
        quality = QUALITY_PREFIX_PONY
        negative = NEGATIVE_PROMPT_PONY
    elif model_preset == "realistic" or (model_preset == "auto" and style == "realistic"):
        quality = QUALITY_PREFIX_DEFAULT
        negative = NEGATIVE_PROMPT_REALISTIC
    else:
        quality = QUALITY_PREFIX_DEFAULT
        negative = NEGATIVE_PROMPT_ANIME

    full_prompt = f"{quality}, {tags}"
    return full_prompt, negative


# ============================================================
# 結果表示
# ============================================================

def display_result(
    prompt: str,
    negative: str,
    style: str,
    copied: bool,
    image_path: str,
) -> None:
    """結果をコンソールに表示する。"""
    sep = "─" * 60
    style_label = "🖼️  Anime / Illustration" if style == "anime" else "📷 Realistic / Photo"

    print(sep)
    print(f"  解析画像 : {Path(image_path).name}")
    print(f"  検出画風 : {style_label}")
    print(sep)
    print()
    print("[🎨 Stable Diffusion Prompt]")
    print(prompt)
    print()
    print("[🚫 Negative Prompt]")
    print(negative)
    print()

    if copied:
        print("✅ Prompt copied to clipboard!")
    elif not CLIPBOARD_AVAILABLE:
        print("💡 pyperclip をインストールすると自動コピーが使えます:")
        print("   pip install pyperclip")
    else:
        print("⚠️  クリップボードへのコピーをスキップしました。")

    print()
    print(sep)


# ============================================================
# コマンドライン引数
# ============================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="sd_vision_pro.py",
        description="SD Vision Pro - 画像を解析してStable Diffusionプロンプトを生成（無料）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
使用例:
  python sd_vision_pro.py photo.jpg
  python sd_vision_pro.py anime.png --model pony
  python sd_vision_pro.py image.webp --model realistic --no-clipboard

モデルプリセット:
  auto      ... 画像の画風を自動判定（デフォルト）
  sdxl      ... Stable Diffusion XL
  sd15      ... Stable Diffusion 1.5
  pony      ... Pony Diffusion V6 XL（score_9ベース）
  realistic ... 実写系モデル（Realistic Visionなど）

APIキー取得（無料・クレジットカード不要）:
  https://aistudio.google.com/

無料枠: 1日1,500リクエスト / 1分15リクエスト
""",
    )
    parser.add_argument(
        "image",
        help="解析する画像ファイルのパス (PNG/JPG/WEBP/GIF/BMP)",
    )
    parser.add_argument(
        "--model",
        choices=["auto", "sdxl", "sd15", "pony", "realistic"],
        default="auto",
        metavar="MODEL",
        help="ターゲットSDモデルプリセット (default: auto)",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="クリップボードへの自動コピーを無効化",
    )
    return parser.parse_args()


# ============================================================
# エントリーポイント
# ============================================================

def main() -> None:
    args = parse_args()

    # APIキー設定
    setup_gemini()

    # 画像読み込み
    img = load_image(args.image)

    # Geminiで解析
    style, raw_tags = analyze_image(img)

    # プロンプト構築
    full_prompt, negative = build_prompt(style, raw_tags, args.model)

    # クリップボードにコピー
    copied = False
    if not args.no_clipboard and CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(full_prompt)
            copied = True
        except Exception:
            pass

    # 結果表示
    display_result(full_prompt, negative, style, copied, args.image)


if __name__ == "__main__":
    main()
