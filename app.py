"""
SD-Prompt-Architect-Pro
Stable Diffusion用 究極のプロンプト生成ツール
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from tags_master import (
    ENHANCEMENT_RULES,
    JA_EN_DICTIONARY,
    MODEL_PRESETS,
    TAG_CATEGORIES,
)

# ============================================================
# 定数・パス
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "history.json"
CUSTOM_DICT_FILE = BASE_DIR / "custom_dictionary.json"

# ============================================================
# ページ設定
# ============================================================
st.set_page_config(
    page_title="SD-Prompt-Architect-Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# カスタムCSS (ダークモード対応)
# ============================================================
st.markdown("""
<style>
    /* ダークモード対応 */
    .stApp {
        font-family: 'Segoe UI', 'Hiragino Sans', 'Meiryo', sans-serif;
    }
    .prompt-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        color: #e0e0e0;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #0f3460;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.8;
        word-wrap: break-word;
        white-space: pre-wrap;
        margin: 10px 0;
    }
    .negative-box {
        background: linear-gradient(135deg, #2e1a1a 0%, #3e1621 100%);
        color: #e0e0e0;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #60200f;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.8;
        word-wrap: break-word;
        white-space: pre-wrap;
        margin: 10px 0;
    }
    .tag-chip {
        display: inline-block;
        background: #0f3460;
        color: #e0e0e0;
        padding: 4px 12px;
        border-radius: 16px;
        margin: 3px;
        font-size: 13px;
        border: 1px solid #1a5276;
    }
    .section-header {
        background: linear-gradient(90deg, #0f3460 0%, transparent 100%);
        padding: 8px 16px;
        border-radius: 8px;
        margin: 16px 0 8px 0;
        font-weight: bold;
        color: #e0e0e0;
    }
    .history-item {
        background: #1a1a2e;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #0f3460;
        margin: 8px 0;
        font-size: 13px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stat-card {
        background: linear-gradient(135deg, #0f3460, #1a5276);
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# ユーティリティ関数
# ============================================================
def load_json(path: Path) -> list | dict:
    """JSONファイルを読み込む"""
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return [] if "history" in str(path) else {}


def save_json(path: Path, data: list | dict) -> None:
    """JSONファイルに保存する"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_custom_dictionary() -> dict[str, str]:
    """カスタム辞書をロードする"""
    return load_json(CUSTOM_DICT_FILE) if CUSTOM_DICT_FILE.exists() else {}


def save_custom_dictionary(d: dict[str, str]) -> None:
    """カスタム辞書を保存する"""
    save_json(CUSTOM_DICT_FILE, d)


def get_full_dictionary() -> dict[str, str]:
    """組み込み辞書 + カスタム辞書を統合して返す"""
    merged = dict(JA_EN_DICTIONARY)
    merged.update(load_custom_dictionary())
    return merged


def translate_japanese_input(text: str) -> list[str]:
    """日本語入力をタグリストに変換する"""
    dictionary = get_full_dictionary()
    # カンマまたは読点で分割
    raw_parts = []
    for part in text.replace("、", ",").replace("　", " ").split(","):
        part = part.strip()
        if part:
            raw_parts.append(part)

    result_tags: list[str] = []
    for part in raw_parts:
        # 辞書で完全一致
        if part in dictionary:
            translated = dictionary[part]
            result_tags.extend(t.strip() for t in translated.split(",") if t.strip())
        else:
            # 部分マッチを試行
            found = False
            for ja, en in dictionary.items():
                if ja in part:
                    result_tags.extend(t.strip() for t in en.split(",") if t.strip())
                    found = True
                    break
            if not found:
                # そのまま（英語タグとして扱う）
                result_tags.append(part)
    return result_tags


def apply_enhancements(tags: list[str]) -> list[str]:
    """タグリストに対して自動補完を適用する"""
    tags_lower = {t.lower() for t in tags}
    suggestions: list[str] = []
    for _rule_name, rule in ENHANCEMENT_RULES.items():
        if any(kw in tag for kw in rule["keywords"] for tag in tags_lower):
            for s in rule["suggestions"]:
                if s.lower() not in tags_lower:
                    suggestions.append(s)
    return suggestions


def build_prompt(
    model: str,
    selected_tags: list[str],
    user_input_tags: list[str],
    use_quality: bool,
    use_enhancement: bool,
) -> tuple[str, str]:
    """最終的なプロンプトとネガティブプロンプトを構築する"""
    preset = MODEL_PRESETS.get(model, MODEL_PRESETS["SDXL"])
    parts: list[str] = []

    # クオリティプレフィックス
    if use_quality:
        parts.extend(preset["quality_prefix"])

    # ユーザー入力タグ
    parts.extend(user_input_tags)

    # 選択済みタグ
    parts.extend(selected_tags)

    # 自動補完
    if use_enhancement:
        enhancements = apply_enhancements(parts)
        parts.extend(enhancements)

    # 重複排除（順序保持）
    seen: set[str] = set()
    unique_parts: list[str] = []
    for tag in parts:
        tag_l = tag.lower().strip()
        if tag_l and tag_l not in seen:
            seen.add(tag_l)
            unique_parts.append(tag.strip())

    prompt = ", ".join(unique_parts)
    negative = preset["negative_prompt"]
    return prompt, negative


def add_to_history(prompt: str, negative: str, model: str) -> None:
    """履歴に追加する"""
    history = load_json(HISTORY_FILE) if HISTORY_FILE.exists() else []
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": model,
        "prompt": prompt,
        "negative": negative,
    }
    history.insert(0, entry)
    # 最大100件に制限
    history = history[:100]
    save_json(HISTORY_FILE, history)


# ============================================================
# セッション状態の初期化
# ============================================================
if "selected_tags" not in st.session_state:
    st.session_state.selected_tags = []
if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""
if "generated_negative" not in st.session_state:
    st.session_state.generated_negative = ""
if "tag_search" not in st.session_state:
    st.session_state.tag_search = ""


# ============================================================
# サイドバー
# ============================================================
with st.sidebar:
    st.markdown("## SD-Prompt-Architect-Pro")
    st.markdown("---")

    # モデル選択
    st.markdown("### モデル選択")
    selected_model = st.selectbox(
        "使用モデル",
        list(MODEL_PRESETS.keys()),
        help="生成に使用するモデルを選択してください",
    )
    preset_info = MODEL_PRESETS[selected_model]
    st.caption(preset_info["description"])

    st.markdown("---")

    # オプション
    st.markdown("### 生成オプション")
    use_quality_prefix = st.checkbox("クオリティタグを自動付与", value=True)
    use_auto_enhance = st.checkbox("AIエンハンサー (自動補完)", value=True)
    nsfw_mode = st.checkbox("NSFWタグを表示", value=False)

    st.markdown("---")

    # 推奨タグ表示
    st.markdown("### モデル推奨タグ")
    for tag in preset_info["recommended_tags"]:
        if st.button(f"+ {tag}", key=f"rec_{tag}", use_container_width=True):
            if tag not in st.session_state.selected_tags:
                st.session_state.selected_tags.append(tag)
                st.rerun()

    st.markdown("---")

    # カスタム辞書管理
    st.markdown("### カスタム辞書管理")
    with st.expander("単語を追加"):
        col_ja, col_en = st.columns(2)
        with col_ja:
            new_ja = st.text_input("日本語", key="dict_ja")
        with col_en:
            new_en = st.text_input("英語タグ", key="dict_en")
        if st.button("辞書に追加", use_container_width=True):
            if new_ja and new_en:
                custom_dict = load_custom_dictionary()
                custom_dict[new_ja] = new_en
                save_custom_dictionary(custom_dict)
                st.success(f"追加: {new_ja} → {new_en}")
            else:
                st.warning("日本語と英語の両方を入力してください")

    with st.expander("登録済み単語一覧"):
        custom_dict = load_custom_dictionary()
        if custom_dict:
            for ja, en in custom_dict.items():
                c1, c2, c3 = st.columns([3, 3, 1])
                c1.write(ja)
                c2.write(en)
                if c3.button("×", key=f"del_{ja}"):
                    del custom_dict[ja]
                    save_custom_dictionary(custom_dict)
                    st.rerun()
        else:
            st.info("カスタム辞書は空です")

    st.markdown("---")
    st.caption("SD-Prompt-Architect-Pro v1.0")


# ============================================================
# メイン画面
# ============================================================
st.markdown("# SD-Prompt-Architect-Pro")
st.markdown("Stable Diffusion用プロンプトを直感的に構築できるツールです。")

# --- 日本語入力エリア ---
st.markdown("---")
st.markdown("### 日本語キーワード入力")
st.caption("日本語でキーワードをカンマ区切りで入力すると、自動的に英語タグに変換されます。")

user_text = st.text_area(
    "キーワード入力",
    placeholder="例: 美少女, 金髪, ロングヘア, 笑顔, 制服, 教室, 柔らかい光",
    height=100,
    label_visibility="collapsed",
)

if user_text:
    translated = translate_japanese_input(user_text)
    if translated:
        st.markdown("**変換結果:**")
        chips_html = " ".join(
            f'<span class="tag-chip">{t}</span>' for t in translated
        )
        st.markdown(chips_html, unsafe_allow_html=True)
else:
    translated = []

# --- タグカテゴリ選択 ---
st.markdown("---")
st.markdown("### タグライブラリ")

# 検索フィルター
tag_search = st.text_input(
    "タグ検索",
    placeholder="タグを検索... (英語/日本語)",
    key="tag_search_input",
)

# カテゴリ表示
for category_name, subcategories in TAG_CATEGORIES.items():
    # NSFWフィルタ
    if "NSFW" in category_name and not nsfw_mode:
        continue

    with st.expander(f"{category_name}", expanded=False):
        for sub_name, tags in subcategories.items():
            # 検索フィルター適用
            if tag_search:
                filtered_tags = [
                    t for t in tags
                    if tag_search.lower() in t.lower()
                ]
                if not filtered_tags:
                    continue
            else:
                filtered_tags = tags

            st.markdown(
                f'<div class="section-header">{sub_name}</div>',
                unsafe_allow_html=True,
            )

            # タグをグリッドで表示
            cols = st.columns(4)
            for i, tag in enumerate(filtered_tags):
                col = cols[i % 4]
                is_selected = tag in st.session_state.selected_tags
                label = f"{'✓ ' if is_selected else ''}{tag}"
                if col.button(
                    label,
                    key=f"tag_{category_name}_{sub_name}_{tag}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                ):
                    if is_selected:
                        st.session_state.selected_tags.remove(tag)
                    else:
                        st.session_state.selected_tags.append(tag)
                    st.rerun()

# --- 選択中のタグ表示 ---
st.markdown("---")
st.markdown("### 選択中のタグ")

if st.session_state.selected_tags:
    # チップ表示
    chips_html = " ".join(
        f'<span class="tag-chip">{t}</span>'
        for t in st.session_state.selected_tags
    )
    st.markdown(chips_html, unsafe_allow_html=True)

    # 個別削除
    st.markdown("")
    remove_cols = st.columns(min(len(st.session_state.selected_tags), 8))
    for i, tag in enumerate(st.session_state.selected_tags):
        col = remove_cols[i % min(len(st.session_state.selected_tags), 8)]
        if col.button(f"× {tag}", key=f"remove_{tag}"):
            st.session_state.selected_tags.remove(tag)
            st.rerun()

    if st.button("全てクリア", type="secondary"):
        st.session_state.selected_tags = []
        st.rerun()
else:
    st.info("タグを選択するか、上のテキストボックスにキーワードを入力してください。")

# --- プロンプト生成 ---
st.markdown("---")
st.markdown("### プロンプト生成")

col_gen1, col_gen2 = st.columns(2)
with col_gen1:
    st.markdown(f"**モデル:** {selected_model}")
with col_gen2:
    tag_count = len(st.session_state.selected_tags) + len(translated)
    st.markdown(f"**タグ数:** {tag_count}")

if st.button("プロンプトを生成", type="primary", use_container_width=True):
    prompt, negative = build_prompt(
        model=selected_model,
        selected_tags=st.session_state.selected_tags,
        user_input_tags=translated,
        use_quality=use_quality_prefix,
        use_enhancement=use_auto_enhance,
    )
    st.session_state.generated_prompt = prompt
    st.session_state.generated_negative = negative

    # 履歴に保存
    if prompt:
        add_to_history(prompt, negative, selected_model)

# --- 生成結果表示 ---
if st.session_state.generated_prompt:
    st.markdown("#### Positive Prompt")
    st.markdown(
        f'<div class="prompt-box">{st.session_state.generated_prompt}</div>',
        unsafe_allow_html=True,
    )
    st.code(st.session_state.generated_prompt, language=None)

    st.markdown("#### Negative Prompt")
    st.markdown(
        f'<div class="negative-box">{st.session_state.generated_negative}</div>',
        unsafe_allow_html=True,
    )
    st.code(st.session_state.generated_negative, language=None)

    # 統計情報
    prompt_tags = [t.strip() for t in st.session_state.generated_prompt.split(",")]
    st.markdown(
        f"""
        <div class="stat-card">
            <strong>生成統計</strong><br>
            タグ数: {len(prompt_tags)} |
            文字数: {len(st.session_state.generated_prompt)} |
            モデル: {selected_model}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- ネガティブプロンプト手動編集 ---
if st.session_state.generated_negative:
    st.markdown("---")
    st.markdown("### ネガティブプロンプト編集")
    edited_negative = st.text_area(
        "ネガティブプロンプトを編集",
        value=st.session_state.generated_negative,
        height=100,
        label_visibility="collapsed",
    )
    if edited_negative != st.session_state.generated_negative:
        st.session_state.generated_negative = edited_negative

# --- 履歴管理 ---
st.markdown("---")
st.markdown("### 生成履歴")

history = load_json(HISTORY_FILE) if HISTORY_FILE.exists() else []

if history:
    for i, entry in enumerate(history[:20]):
        with st.expander(
            f"{entry['timestamp']} | {entry['model']} | "
            f"{entry['prompt'][:60]}...",
            expanded=False,
        ):
            st.markdown("**Positive:**")
            st.code(entry["prompt"], language=None)
            st.markdown("**Negative:**")
            st.code(entry["negative"], language=None)

            col_h1, col_h2 = st.columns(2)
            with col_h1:
                if st.button("このプロンプトを復元", key=f"restore_{i}"):
                    st.session_state.generated_prompt = entry["prompt"]
                    st.session_state.generated_negative = entry["negative"]
                    st.rerun()
            with col_h2:
                if st.button("履歴から削除", key=f"del_hist_{i}"):
                    history.pop(i)
                    save_json(HISTORY_FILE, history)
                    st.rerun()

    if st.button("履歴を全て削除", type="secondary"):
        save_json(HISTORY_FILE, [])
        st.rerun()
else:
    st.info("まだ生成履歴はありません。プロンプトを生成すると自動的に保存されます。")
