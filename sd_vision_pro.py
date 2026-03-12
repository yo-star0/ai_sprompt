#!/usr/bin/env python3
"""
SD Vision Pro - Stable Diffusion用 画像解析・プロンプト生成ツール

画像をClaude Vision APIで解析し、SDでそのまま使えるプロンプトを自動生成します。

必要なライブラリのインストール:
    pip install anthropic Pillow pyperclip

使い方:
    python sd_vision_pro.py image.png
    python sd_vision_pro.py photo.jpg --model sdxl
    python sd_vision_pro.py illustration.png --model pony
    python sd_vision_pro.py image.png --no-clipboard
"""

import argparse
import base64
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("Error: anthropic ライブラリが必要です。")
    print("  pip install anthropic")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow ライブラリが必要です。")
    print("  pip install Pillow")
    sys.exit(1)

try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


# ============================================================
# 定数
# ============================================================

QUALITY_PREFIX = "(best quality:1.2), masterpiece, highres"

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

MODEL_NEGATIVE_OVERRIDES = {
    "pony": (
        "score_1, score_2, score_3, score_4, score_5, "
        "lowres, bad anatomy, bad hands, text, error, "
        "missing fingers, extra digit, fewer digits, "
        "cropped, worst quality, low quality, normal quality, "
        "jpeg artifacts, signature, watermark, username, blurry, "
        "deformed, disfigured, mutation, ugly"
    ),
}

VISION_SYSTEM_PROMPT = """\
You are an expert Stable Diffusion prompt engineer with deep knowledge of \
image composition, art styles, and SD tag conventions.

Your task: Analyze the provided image and generate a precise, \
comma-separated English tag prompt that can reproduce it in Stable Diffusion.

## Rules

1. **Style Detection**: First determine if the image is:
   - "anime" (anime, illustration, cartoon, manga, digital art)
   - "realistic" (photograph, photorealistic render, real person)
   Output this as the first line: `STYLE: anime` or `STYLE: realistic`

2. **Tag Extraction**: Extract ALL relevant details as SD-compatible tags:
   - **Subject**: gender, number of people, age impression (1girl, 1boy, solo, etc.)
   - **Hair**: style, length, color (e.g., long hair, blonde hair, ponytail)
   - **Eyes**: color, shape (e.g., blue eyes, detailed eyes)
   - **Face/Expression**: emotion, details (e.g., smile, blush, looking at viewer)
   - **Body**: type, notable features (e.g., slender, petite)
   - **Clothing**: full outfit description (e.g., school uniform, white shirt, pleated skirt)
   - **Accessories**: jewelry, headwear, etc. (e.g., hair ribbon, glasses, choker)
   - **Pose**: body position, hand placement (e.g., standing, hand on hip, peace sign)
   - **Composition**: camera angle, framing (e.g., upper body, from above, close-up)
   - **Background**: setting, environment (e.g., classroom, cherry blossoms, night city)
   - **Lighting**: type, direction (e.g., soft lighting, backlighting, golden hour)
   - **Effects**: particles, atmosphere (e.g., bokeh, sparkles, lens flare)
   - **Art style specifics**: if anime, note the style cues (e.g., cel shading, vibrant colors)
   - **Photo specifics**: if realistic, note camera cues (e.g., shallow depth of field, 85mm lens, film grain)

3. **Weighting**: Apply (tag:weight) for especially prominent features:
   - Very prominent / defining features: (tag:1.3)
   - Clearly visible important features: (tag:1.2)
   - Notable features: (tag:1.1)
   - Standard features: no weight needed

4. **Output Format**:
   Line 1: `STYLE: anime` or `STYLE: realistic`
   Line 2: Empty line
   Line 3: The complete comma-separated tag prompt (NO quality prefix, I will add that)

   Output ONLY these 3 lines. No explanations, no markdown, no extra text.

5. **Quality Guidelines**:
   - Use established SD/Danbooru tag conventions
   - Be specific: prefer "pleated skirt" over "skirt"
   - Include 20-50 tags for thorough coverage
   - Order: subject → appearance → clothing → pose → composition → background → lighting → effects
"""


# ============================================================
# 画像読み込み
# ============================================================


def load_image_as_base64(image_path: str) -> tuple[str, str]:
    """画像ファイルを読み込み、Base64エンコードとメディアタイプを返す。"""
    path = Path(image_path)
    if not path.exists():
        print(f"Error: ファイルが見つかりません: {image_path}")
        sys.exit(1)

    # Pillowで画像を検証
    try:
        img = Image.open(path)
        img.verify()
    except Exception as e:
        print(f"Error: 画像ファイルの読み込みに失敗しました: {e}")
        sys.exit(1)

    # メディアタイプを決定
    suffix = path.suffix.lower()
    media_type_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(suffix)
    if not media_type:
        print(f"Error: サポートされていない画像形式です: {suffix}")
        print("  対応形式: PNG, JPG, JPEG, GIF, WEBP")
        sys.exit(1)

    # Base64エンコード
    with open(path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return image_data, media_type


# ============================================================
# Claude Vision API 呼び出し
# ============================================================


def analyze_image(image_data: str, media_type: str) -> tuple[str, str]:
    """Claude Vision APIで画像を解析し、(style, prompt)のタプルを返す。"""
    client = anthropic.Anthropic()

    print("🔍 画像を解析中...")
    print()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Analyze this image and generate a Stable Diffusion prompt following the rules in your system prompt.",
                    },
                ],
            }
        ],
        system=VISION_SYSTEM_PROMPT,
    )

    response_text = message.content[0].text.strip()

    # レスポンスをパース
    lines = [line.strip() for line in response_text.split("\n") if line.strip()]

    style = "anime"  # デフォルト
    prompt_tags = ""

    for line in lines:
        if line.upper().startswith("STYLE:"):
            style_value = line.split(":", 1)[1].strip().lower()
            if "realistic" in style_value or "photo" in style_value:
                style = "realistic"
            else:
                style = "anime"
        elif not line.upper().startswith("STYLE:"):
            # STYLE行以外で最も長い行をプロンプトとみなす
            if len(line) > len(prompt_tags):
                prompt_tags = line

    return style, prompt_tags


# ============================================================
# プロンプト構築
# ============================================================


def build_full_prompt(style: str, raw_tags: str, model: str) -> tuple[str, str]:
    """品質タグ付きの完全なプロンプトとネガティブプロンプトを構築する。"""
    # 品質プレフィックス（モデル別）
    if model == "pony":
        quality = "score_9, score_8_up, score_7_up, score_6_up"
    else:
        quality = QUALITY_PREFIX

    # タグの前後空白を正規化
    tags = ", ".join(t.strip() for t in raw_tags.split(",") if t.strip())

    full_prompt = f"{quality}, {tags}"

    # ネガティブプロンプト選択
    if model in MODEL_NEGATIVE_OVERRIDES:
        negative = MODEL_NEGATIVE_OVERRIDES[model]
    elif style == "realistic":
        negative = NEGATIVE_PROMPT_REALISTIC
    else:
        negative = NEGATIVE_PROMPT_ANIME

    return full_prompt, negative


# ============================================================
# 出力
# ============================================================


def display_result(prompt: str, negative: str, copied: bool) -> None:
    """結果をコンソールに表示する。"""
    separator = "─" * 60

    print(separator)
    print()
    print("[🎨 Stable Diffusion Prompt]")
    print(prompt)
    print()
    print("[🚫 Negative Prompt]")
    print(negative)
    print()

    if copied:
        print("✅ Prompt copied to clipboard!")
    else:
        print("⚠️  クリップボードへのコピーはスキップされました。")
        if not CLIPBOARD_AVAILABLE:
            print("   pyperclip をインストールすると自動コピーが有効になります:")
            print("   pip install pyperclip")

    print()
    print(separator)


# ============================================================
# メイン
# ============================================================


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SD Vision Pro - 画像解析からStable Diffusionプロンプトを生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
使用例:
  python sd_vision_pro.py photo.jpg
  python sd_vision_pro.py anime.png --model pony
  python sd_vision_pro.py image.webp --no-clipboard

対応画像形式: PNG, JPG, JPEG, GIF, WEBP

環境変数:
  ANTHROPIC_API_KEY  Claude APIキーを設定してください
""",
    )
    parser.add_argument(
        "image",
        help="解析する画像ファイルのパス",
    )
    parser.add_argument(
        "--model",
        choices=["sdxl", "sd15", "pony", "realistic"],
        default="sdxl",
        help="ターゲットSDモデル (default: sdxl)",
    )
    parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="クリップボードへのコピーを無効化",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # 画像読み込み
    image_data, media_type = load_image_as_base64(args.image)

    # Claude Vision APIで解析
    style, raw_tags = analyze_image(image_data, media_type)

    # プロンプト構築
    full_prompt, negative = build_full_prompt(style, raw_tags, args.model)

    # クリップボードにコピー
    copied = False
    if not args.no_clipboard and CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(full_prompt)
            copied = True
        except pyperclip.PyperclipException:
            pass

    # 結果表示
    display_result(full_prompt, negative, copied)


if __name__ == "__main__":
    main()
