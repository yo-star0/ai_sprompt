"""
SD-Prompt-Architect-Pro: Tags Master Database
膨大なタグデータを保持するモジュール
"""

# ============================================================
# 日本語 → 英語 変換辞書
# ============================================================
JA_EN_DICTIONARY: dict[str, str] = {
    # --- 人物・基本 ---
    "女の子": "girl",
    "少女": "girl",
    "女性": "woman",
    "男の子": "boy",
    "少年": "boy",
    "男性": "man",
    "一人": "solo",
    "二人": "2girls",
    "カップル": "couple",
    "美少女": "beautiful girl",
    "美女": "beautiful woman",
    "可愛い": "cute",
    "綺麗": "beautiful",
    "セクシー": "sexy",
    # --- 髪型・髪色 ---
    "ロングヘア": "long hair",
    "長い髪": "long hair",
    "ショートヘア": "short hair",
    "短い髪": "short hair",
    "ミディアムヘア": "medium hair",
    "ポニーテール": "ponytail",
    "ツインテール": "twintails",
    "お団子": "hair bun",
    "三つ編み": "braid",
    "サイドテール": "side ponytail",
    "前髪": "bangs",
    "ぱっつん": "blunt bangs",
    "金髪": "blonde hair",
    "黒髪": "black hair",
    "茶髪": "brown hair",
    "赤髪": "red hair",
    "銀髪": "silver hair",
    "白髪": "white hair",
    "青髪": "blue hair",
    "ピンク髪": "pink hair",
    "紫髪": "purple hair",
    "緑髪": "green hair",
    "グラデーション": "gradient hair",
    "メッシュ": "streaked hair",
    # --- 目 ---
    "青い目": "blue eyes",
    "赤い目": "red eyes",
    "緑の目": "green eyes",
    "茶色の目": "brown eyes",
    "金色の目": "golden eyes",
    "紫の目": "purple eyes",
    "オッドアイ": "heterochromia",
    "猫目": "cat eyes",
    "ジト目": "half-closed eyes",
    "輝く目": "sparkling eyes",
    # --- 体型・身体 ---
    "スレンダー": "slender",
    "スリム": "slim",
    "グラマー": "curvy",
    "筋肉質": "muscular",
    "小柄": "petite",
    "長身": "tall",
    "巨乳": "large breasts",
    "貧乳": "flat chest",
    "普通体型": "medium breasts",
    "美脚": "beautiful legs",
    "美尻": "beautiful butt",
    "腹筋": "abs",
    "くびれ": "narrow waist",
    "太もも": "thighs",
    # --- 表情 ---
    "笑顔": "smile",
    "微笑み": "gentle smile",
    "照れ": "blush",
    "泣き顔": "crying",
    "驚き": "surprised",
    "怒り": "angry",
    "無表情": "expressionless",
    "恥ずかしい": "embarrassed",
    "上目遣い": "looking up",
    "ウインク": "wink",
    "舌出し": "tongue out",
    "口開け": "open mouth",
    "半目": "half-closed eyes",
    "目を閉じる": "closed eyes",
    "涙": "tears",
    "赤面": "blush",
    # --- 服装 ---
    "制服": "school uniform",
    "セーラー服": "sailor uniform",
    "ブレザー": "blazer",
    "ワンピース": "dress",
    "ドレス": "dress",
    "ウェディングドレス": "wedding dress",
    "メイド服": "maid outfit",
    "水着": "swimsuit",
    "ビキニ": "bikini",
    "体操服": "gym uniform",
    "ブルマ": "bloomers",
    "着物": "kimono",
    "浴衣": "yukata",
    "チャイナドレス": "china dress",
    "ナース服": "nurse outfit",
    "軍服": "military uniform",
    "スーツ": "business suit",
    "パーカー": "hoodie",
    "Tシャツ": "t-shirt",
    "タンクトップ": "tank top",
    "ミニスカート": "miniskirt",
    "ロングスカート": "long skirt",
    "ショートパンツ": "shorts",
    "ジーンズ": "jeans",
    "レオタード": "leotard",
    "バニースーツ": "bunny suit",
    "サンタ服": "santa costume",
    "魔女": "witch outfit",
    "鎧": "armor",
    "白衣": "lab coat",
    "エプロン": "apron",
    "オーバーオール": "overalls",
    "ニーソックス": "thigh highs",
    "ストッキング": "stockings",
    "タイツ": "pantyhose",
    "ガーターベルト": "garter belt",
    "手袋": "gloves",
    "ブーツ": "boots",
    "ハイヒール": "high heels",
    "スニーカー": "sneakers",
    "リボン": "ribbon",
    "ネクタイ": "necktie",
    "チョーカー": "choker",
    "眼鏡": "glasses",
    "サングラス": "sunglasses",
    "帽子": "hat",
    "ヘッドバンド": "headband",
    "ティアラ": "tiara",
    "猫耳": "cat ears",
    "うさ耳": "rabbit ears",
    "ヘッドホン": "headphones",
    "イヤリング": "earrings",
    "ネックレス": "necklace",
    "ブレスレット": "bracelet",
    "指輪": "ring",
    # --- NSFW衣装 ---
    "ランジェリー": "lingerie",
    "下着": "underwear",
    "ブラジャー": "bra",
    "パンツ": "panties",
    "Tバック": "thong",
    "紐パン": "string panties",
    "裸": "nude",
    "全裸": "completely nude",
    "半裸": "partially nude",
    "裸エプロン": "naked apron",
    "裸ワイシャツ": "naked shirt",
    "タオル一枚": "towel only",
    "透け": "see-through",
    "透け下着": "see-through underwear",
    "マイクロビキニ": "micro bikini",
    "スリングビキニ": "sling bikini",
    "ボディスーツ": "bodysuit",
    "ボンデージ": "bondage outfit",
    "ラバースーツ": "latex suit",
    # --- NSFW状態 ---
    "脱ぎかけ": "undressing",
    "はだけた": "clothes falling off",
    "ずり落ち": "clothes sliding down",
    "服破れ": "torn clothes",
    "服引っ張り": "clothes pull",
    "スカートめくり": "skirt lift",
    "胸チラ": "cleavage peek",
    "パンチラ": "panty peek",
    "横乳": "sideboob",
    "下乳": "underboob",
    "ノーブラ": "no bra",
    "ノーパン": "no panties",
    # --- NSFWポーズ・体位 ---
    "四つん這い": "all fours",
    "開脚": "spread legs",
    "M字開脚": "m-legs spread",
    "仰向け": "lying on back",
    "うつ伏せ": "lying on stomach",
    "膝立ち": "kneeling",
    "跪く": "on knees",
    "しゃがむ": "squatting",
    "屈む": "bent over",
    "抱き合う": "hugging",
    "背面座位": "reverse sitting",
    "正常位": "missionary",
    "騎乗位": "cowgirl position",
    "バック": "from behind",
    "立位": "standing position",
    "側位": "spooning",
    "座位": "sitting position",
    # --- NSFWシチュエーション ---
    "拘束": "restraints",
    "縛り": "bondage",
    "手錠": "handcuffs",
    "目隠し": "blindfold",
    "首輪": "collar",
    "鎖": "chains",
    "触手": "tentacles",
    "野外露出": "outdoor exposure",
    "公共": "public",
    "温泉": "onsen",
    "お風呂": "bath",
    "シャワー": "shower",
    "プール": "pool",
    "ベッド": "on bed",
    "教室": "classroom",
    "更衣室": "locker room",
    "トイレ": "restroom",
    # --- ポーズ ---
    "立ち": "standing",
    "座り": "sitting",
    "膝つき": "kneeling",
    "横たわる": "lying down",
    "走る": "running",
    "歩く": "walking",
    "ジャンプ": "jumping",
    "飛ぶ": "flying",
    "振り向き": "looking back",
    "手を振る": "waving",
    "ピース": "peace sign",
    "腕組み": "arms crossed",
    "手を腰に": "hand on hip",
    "頬杖": "chin rest",
    "髪をかきあげる": "hair flip",
    "ストレッチ": "stretching",
    "寄りかかる": "leaning",
    # --- 構図 ---
    "アップ": "close-up",
    "顔アップ": "face close-up",
    "バストアップ": "upper body",
    "全身": "full body",
    "ロングショット": "wide shot",
    "俯瞰": "from above",
    "煽り": "from below",
    "横顔": "profile",
    "後ろ姿": "from behind",
    "ダッチアングル": "dutch angle",
    "魚眼": "fisheye",
    "鳥瞰": "bird's eye view",
    "正面": "front view",
    # --- 背景・場所 ---
    "白背景": "white background",
    "シンプル背景": "simple background",
    "グラデーション背景": "gradient background",
    "教室": "classroom",
    "学校": "school",
    "街": "city",
    "夜の街": "night city",
    "サイバーパンク": "cyberpunk city",
    "海": "ocean",
    "ビーチ": "beach",
    "森": "forest",
    "花畑": "flower field",
    "桜": "cherry blossoms",
    "紅葉": "autumn leaves",
    "雪景色": "snowy landscape",
    "夕焼け": "sunset",
    "星空": "starry sky",
    "月明かり": "moonlight",
    "部屋": "room",
    "寝室": "bedroom",
    "リビング": "living room",
    "キッチン": "kitchen",
    "カフェ": "cafe",
    "図書館": "library",
    "教会": "church",
    "城": "castle",
    "廃墟": "ruins",
    "宇宙": "space",
    "異世界": "fantasy world",
    "天国": "heaven",
    "地獄": "hell",
    "水中": "underwater",
    "空": "sky",
    "雲の上": "above clouds",
    # --- 照明・光 ---
    "自然光": "natural lighting",
    "夕日光": "golden hour",
    "逆光": "backlighting",
    "サイドライト": "side lighting",
    "スポットライト": "spotlight",
    "ネオン": "neon lighting",
    "キャンドル": "candlelight",
    "日光": "sunlight",
    "木漏れ日": "dappled sunlight",
    "柔らかい光": "soft lighting",
    "劇的な光": "dramatic lighting",
    "暗い": "dark",
    "明るい": "bright",
    "影": "shadow",
    "光芒": "light rays",
    "レンズフレア": "lens flare",
    "玉ボケ": "bokeh",
    # --- 画風・スタイル ---
    "アニメ風": "anime style",
    "リアル": "realistic",
    "油絵風": "oil painting",
    "水彩画": "watercolor",
    "鉛筆画": "pencil drawing",
    "デジタルアート": "digital art",
    "コンセプトアート": "concept art",
    "浮世絵": "ukiyo-e",
    "ファンタジー": "fantasy",
    "SF": "sci-fi",
    "スチームパンク": "steampunk",
    "ゴシック": "gothic",
    "ポップアート": "pop art",
    "印象派": "impressionist",
    "ミニマリスト": "minimalist",
    "アールヌーボー": "art nouveau",
    "サイケデリック": "psychedelic",
    "ピクセルアート": "pixel art",
    "3DCG": "3d render",
    "写真": "photograph",
    "イラスト": "illustration",
    # --- クオリティ ---
    "高品質": "masterpiece, best quality",
    "傑作": "masterpiece",
    "超高画質": "8k wallpaper, ultra highres",
    "精密": "highly detailed",
    "美麗": "beautiful detailed",
    "鮮明": "sharp focus",
    "プロ品質": "professional",
    # --- 季節・天候 ---
    "春": "spring",
    "夏": "summer",
    "秋": "autumn",
    "冬": "winter",
    "雨": "rain",
    "雪": "snow",
    "嵐": "storm",
    "霧": "fog",
    "虹": "rainbow",
    "曇り": "cloudy",
    "晴れ": "sunny",
    # --- 小物・アクセサリー ---
    "剣": "sword",
    "魔法の杖": "magic wand",
    "銃": "gun",
    "本": "book",
    "花束": "bouquet",
    "傘": "umbrella",
    "カバン": "bag",
    "スマホ": "smartphone",
    "カメラ": "camera",
    "マイク": "microphone",
    "ギター": "guitar",
    "翼": "wings",
    "天使の輪": "halo",
    "悪魔の角": "demon horns",
    "尻尾": "tail",
    "ぬいぐるみ": "plush toy",
    "風船": "balloon",
    "食べ物": "food",
    "ケーキ": "cake",
    "アイスクリーム": "ice cream",
    "お酒": "alcohol",
}

# ============================================================
# カテゴリ別タグプリセット
# ============================================================
TAG_CATEGORIES: dict[str, dict[str, list[str]]] = {
    # ===========================================
    # クオリティ・基本
    # ===========================================
    "クオリティ (Quality)": {
        "最高品質": [
            "masterpiece", "best quality", "ultra highres", "8k wallpaper",
            "extremely detailed", "beautiful detailed", "absurdres",
        ],
        "高品質": [
            "masterpiece", "best quality", "highres", "extremely detailed",
        ],
        "標準品質": [
            "best quality", "highres", "detailed",
        ],
    },

    # ===========================================
    # 実写系 (Photorealistic)
    # ===========================================
    "実写系 (Photorealistic)": {
        "基本実写": [
            "photorealistic", "raw photo", "realistic",
            "8k uhd", "dslr", "high quality", "film grain",
        ],
        "スタジオ撮影": [
            "studio lighting", "professional photography",
            "softbox lighting", "key light", "fill light",
            "beauty dish", "fashion photography", "magazine quality",
        ],
        "ストリートスナップ": [
            "street photography", "candid shot", "natural lighting",
            "35mm film", "kodak portra 400", "fujifilm superia",
            "grain", "light leak",
        ],
        "ポートレート": [
            "portrait photography", "shallow depth of field",
            "85mm lens", "f/1.4", "bokeh", "sharp focus on face",
            "soft skin", "natural skin texture",
        ],
        "カメラ設定": [
            "dslr", "canon eos r5", "sony a7r iv", "nikon z9",
            "fujifilm xt4", "hasselblad", "leica",
            "50mm lens", "85mm lens", "35mm lens", "135mm lens",
            "wide angle", "telephoto", "macro lens",
        ],
        "フィルム風": [
            "film grain", "kodak portra", "fujifilm", "cinestill 800t",
            "analog photo", "vintage photo", "retro",
            "light leak", "color grading", "warm tones",
        ],
        "テクスチャ・質感": [
            "highly detailed texture", "skin pores", "skin texture",
            "fabric texture", "hair detail", "eye detail",
            "subsurface scattering", "natural imperfections",
        ],
        "ライティング(実写)": [
            "soft lighting", "natural light", "golden hour",
            "blue hour", "rim lighting", "rembrandt lighting",
            "butterfly lighting", "split lighting",
            "volumetric lighting", "god rays", "chiaroscuro",
            "high key", "low key",
        ],
    },

    # ===========================================
    # アニメ・イラスト系
    # ===========================================
    "アニメ・イラスト系": {
        "アニメ基本": [
            "anime style", "anime", "cel shading",
            "clean lines", "vibrant colors",
        ],
        "人気画風": [
            "makoto shinkai style", "ghibli style", "kyoto animation style",
            "ufotable style", "trigger style", "shaft style",
        ],
        "イラスト高品質": [
            "illustration", "digital art", "artstation",
            "pixiv ranking", "trending on pixiv",
            "beautiful detailed eyes", "intricate details",
        ],
        "デジタルペインティング": [
            "digital painting", "concept art", "artstation",
            "deviantart", "cgsociety", "award winning",
        ],
        "水彩・油絵風": [
            "watercolor", "oil painting", "gouache",
            "acrylic painting", "impasto", "palette knife",
        ],
    },

    # ===========================================
    # 人物描写
    # ===========================================
    "人物 (Character)": {
        "年齢・人数": [
            "1girl", "1boy", "solo", "2girls", "multiple girls",
            "young woman", "mature female", "teen", "child",
            "couple", "group",
        ],
        "髪型": [
            "long hair", "short hair", "medium hair",
            "ponytail", "twintails", "braid", "side braid",
            "hair bun", "messy hair", "straight hair",
            "wavy hair", "curly hair", "drill hair",
            "hime cut", "bob cut", "pixie cut",
            "ahoge", "hair over one eye", "sidelocks",
            "floating hair", "hair ribbon",
        ],
        "髪色": [
            "blonde hair", "black hair", "brown hair",
            "red hair", "silver hair", "white hair",
            "blue hair", "pink hair", "purple hair",
            "green hair", "orange hair", "grey hair",
            "multicolored hair", "gradient hair", "streaked hair",
        ],
        "目": [
            "blue eyes", "red eyes", "green eyes", "brown eyes",
            "golden eyes", "purple eyes", "pink eyes",
            "heterochromia", "slit pupils", "sparkling eyes",
            "detailed eyes", "beautiful eyes",
        ],
        "表情": [
            "smile", "grin", "gentle smile", "smirk",
            "blush", "embarrassed", "crying",
            "surprised", "angry", "scared",
            "expressionless", "looking at viewer",
            "closed eyes", "half-closed eyes",
            "wink", "tongue out", "open mouth",
            "licking lips", "biting lip", "pout",
            "seductive smile", "ahegao",
        ],
        "体型": [
            "slender", "slim", "petite", "curvy",
            "muscular", "tall", "short",
            "large breasts", "medium breasts", "small breasts", "flat chest",
            "wide hips", "narrow waist", "thick thighs",
            "long legs", "abs",
        ],
    },

    # ===========================================
    # 衣装
    # ===========================================
    "衣装 (Outfit)": {
        "日常服": [
            "casual clothes", "t-shirt", "jeans", "hoodie",
            "sweater", "cardigan", "shorts", "tank top",
            "sundress", "overalls", "jacket",
        ],
        "制服・フォーマル": [
            "school uniform", "sailor uniform", "blazer",
            "business suit", "formal dress", "evening gown",
            "wedding dress", "tuxedo", "military uniform",
        ],
        "コスチューム": [
            "maid outfit", "nurse outfit", "bunny suit",
            "santa costume", "witch outfit", "magical girl",
            "china dress", "kimono", "yukata",
            "armor", "knight", "princess",
            "idol costume", "cheerleader", "police uniform",
        ],
        "スポーツウェア": [
            "gym uniform", "bloomers", "leotard",
            "swimsuit", "bikini", "one-piece swimsuit",
            "competition swimsuit", "sports bra",
            "yoga pants", "tennis outfit",
        ],
        "靴・靴下": [
            "thigh highs", "knee highs", "ankle socks",
            "stockings", "pantyhose", "fishnet stockings",
            "boots", "high heels", "sneakers",
            "sandals", "barefoot", "slippers",
        ],
        "アクセサリー": [
            "glasses", "sunglasses", "choker", "necklace",
            "earrings", "bracelet", "ring", "hair ribbon",
            "headband", "tiara", "crown", "hat", "beret",
            "hair clip", "hair flower", "scrunchie",
            "cat ears", "rabbit ears", "horns",
            "halo", "wings",
        ],
    },

    # ===========================================
    # NSFW カテゴリ
    # ===========================================
    "NSFW - 露出度": {
        "軽度露出": [
            "cleavage", "midriff", "bare shoulders",
            "off shoulder", "sideboob", "underboob",
            "miniskirt", "short shorts", "crop top",
        ],
        "下着・ランジェリー": [
            "lingerie", "underwear", "bra", "panties",
            "lace lingerie", "babydoll", "negligee",
            "corset", "garter belt", "garter straps",
            "thong", "string panties", "strapless bra",
        ],
        "水着(際どい)": [
            "micro bikini", "sling bikini", "string bikini",
            "thong bikini", "see-through swimsuit",
            "body paint swimsuit",
        ],
        "透け・シースルー": [
            "see-through", "see-through dress", "see-through shirt",
            "see-through underwear", "wet clothes",
            "wet t-shirt", "soaked clothes",
        ],
        "裸体": [
            "nude", "completely nude", "partially nude",
            "topless", "bottomless", "naked",
            "naked apron", "naked shirt", "naked towel",
            "covered nipples", "convenient censoring",
            "hair censor", "hand bra",
        ],
    },
    "NSFW - ポーズ・体位": {
        "誘惑ポーズ": [
            "seductive pose", "alluring", "bedroom eyes",
            "come hither", "presenting", "posing",
            "hand on chest", "hand between legs",
            "hip thrust", "arched back",
        ],
        "基本体位": [
            "all fours", "spread legs", "m-legs",
            "lying on back", "lying on stomach",
            "kneeling", "squatting", "bent over",
            "straddling", "sitting on lap",
        ],
        "高度な体位": [
            "missionary", "cowgirl position", "reverse cowgirl",
            "from behind", "standing position",
            "spooning", "sitting position", "suspended",
            "legs up", "face down",
        ],
        "グラビアポーズ": [
            "ass focus", "breast focus", "thigh focus",
            "back focus", "navel focus",
            "leaning forward", "hands on knees",
            "looking back", "over shoulder",
        ],
    },
    "NSFW - シチュエーション": {
        "拘束・ボンデージ": [
            "bondage", "restraints", "handcuffs",
            "rope bondage", "shibari", "tied up",
            "blindfold", "collar", "leash",
            "chains", "spreader bar", "ball gag",
        ],
        "場所・シチュ": [
            "outdoor exposure", "public", "exhibitionism",
            "onsen", "bath", "shower",
            "pool", "on bed", "classroom",
            "locker room", "office",
        ],
        "衣装破壊": [
            "torn clothes", "clothes pull", "skirt lift",
            "shirt lift", "dress pull", "panty pull",
            "bra pull", "undressing", "stripping",
            "clothes ripping", "bursting clothes",
        ],
        "特殊表現": [
            "tentacles", "monster", "orc",
            "sweat", "steam", "saliva",
            "body oil", "lotion",
        ],
    },

    # ===========================================
    # ポーズ・構図
    # ===========================================
    "ポーズ・構図": {
        "基本ポーズ": [
            "standing", "sitting", "kneeling", "lying down",
            "running", "walking", "jumping", "flying",
            "leaning", "crouching", "floating",
        ],
        "手のポーズ": [
            "peace sign", "waving", "pointing",
            "hands up", "arms crossed", "hand on hip",
            "hand on cheek", "finger to mouth",
            "heart hands", "reaching out",
        ],
        "構図": [
            "close-up", "face close-up", "upper body",
            "cowboy shot", "full body", "wide shot",
            "from above", "from below", "from side",
            "from behind", "dutch angle", "fisheye",
            "bird's eye view", "profile", "front view",
            "dynamic angle", "dramatic angle",
        ],
        "カメラアングル": [
            "pov", "selfie", "mirror reflection",
            "split screen", "multiple views",
            "panoramic", "cinematic composition",
        ],
    },

    # ===========================================
    # 背景・環境
    # ===========================================
    "背景・環境 (Background)": {
        "シンプル背景": [
            "white background", "black background",
            "simple background", "gradient background",
            "grey background", "blue background",
            "colorful background",
        ],
        "自然": [
            "outdoors", "nature", "forest", "mountain",
            "ocean", "beach", "lake", "river",
            "flower field", "garden", "meadow",
            "cherry blossoms", "autumn leaves",
            "snowy landscape", "desert", "volcano",
        ],
        "都市": [
            "cityscape", "city", "night city",
            "rooftop", "street", "alley",
            "neon lights", "tokyo", "cyberpunk city",
            "futuristic city", "steampunk city",
        ],
        "屋内": [
            "indoors", "room", "bedroom", "living room",
            "kitchen", "bathroom", "classroom",
            "library", "cafe", "restaurant",
            "church", "castle interior", "dungeon",
            "laboratory", "office", "train",
        ],
        "ファンタジー": [
            "fantasy world", "magical forest",
            "floating island", "crystal cave",
            "dragon's lair", "elven city",
            "heaven", "hell", "underworld",
            "space", "alien planet", "nebula",
        ],
        "天候・空": [
            "sunny", "cloudy", "rainy", "snowy",
            "stormy", "foggy", "sunset", "sunrise",
            "starry sky", "milky way", "aurora",
            "moonlight", "rainbow", "lightning",
        ],
    },

    # ===========================================
    # 照明・エフェクト
    # ===========================================
    "照明・エフェクト": {
        "照明": [
            "natural lighting", "soft lighting",
            "dramatic lighting", "cinematic lighting",
            "rim lighting", "backlighting",
            "side lighting", "volumetric lighting",
            "god rays", "spotlight", "neon lighting",
            "candlelight", "firelight",
        ],
        "エフェクト": [
            "particles", "sparkles", "glowing",
            "magic effects", "fire", "ice",
            "electricity", "smoke", "mist",
            "petals", "feathers", "bubbles",
            "confetti", "snow particles",
        ],
        "色調": [
            "warm colors", "cool colors", "pastel colors",
            "vibrant colors", "muted colors", "monochrome",
            "sepia", "high contrast", "low contrast",
            "color splash", "color grading",
        ],
        "被写界深度": [
            "depth of field", "shallow depth of field",
            "bokeh", "blurry background",
            "tilt shift", "sharp focus",
            "everything in focus", "motion blur",
        ],
    },
}


# ============================================================
# モデル別最適化プリセット
# ============================================================
MODEL_PRESETS: dict[str, dict] = {
    "Pony Diffusion V6": {
        "quality_prefix": [
            "score_9", "score_8_up", "score_7_up", "score_6_up",
        ],
        "recommended_tags": [
            "source_anime", "rating_explicit", "rating_questionable", "rating_safe",
        ],
        "negative_prompt": (
            "score_1, score_2, score_3, score_4, score_5, "
            "lowres, bad anatomy, bad hands, text, error, "
            "missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, "
            "normal quality, jpeg artifacts, signature, "
            "watermark, username, blurry, artist name, "
            "deformed, disfigured, mutation, ugly"
        ),
        "description": "Pony Diffusion V6 XL - アニメ/実写両対応、スコアベースのクオリティ制御",
    },
    "SDXL": {
        "quality_prefix": [
            "masterpiece", "best quality", "ultra highres",
            "8k wallpaper", "absurdres",
        ],
        "recommended_tags": [
            "extremely detailed", "beautiful detailed",
            "intricate details", "sharp focus",
        ],
        "negative_prompt": (
            "lowres, bad anatomy, bad hands, text, error, "
            "missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, "
            "normal quality, jpeg artifacts, signature, "
            "watermark, username, blurry, "
            "deformed, disfigured, mutation, mutated, ugly, "
            "extra limbs, missing limbs, floating limbs, "
            "disconnected limbs, malformed hands, "
            "long neck, long body"
        ),
        "description": "Stable Diffusion XL - 高解像度・高品質生成",
    },
    "SD 1.5": {
        "quality_prefix": [
            "masterpiece", "best quality", "highres",
            "extremely detailed",
        ],
        "recommended_tags": [
            "detailed", "sharp focus", "beautiful",
            "illustration",
        ],
        "negative_prompt": (
            "lowres, bad anatomy, bad hands, text, error, "
            "missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, "
            "normal quality, jpeg artifacts, signature, "
            "watermark, username, blurry, "
            "simple background, monochrome, "
            "bad proportions, gross proportions, "
            "poorly drawn, bad artist"
        ),
        "description": "Stable Diffusion 1.5 - 最も広く使われるベースモデル",
    },
    "実写モデル (Realistic)": {
        "quality_prefix": [
            "photorealistic", "raw photo", "8k uhd",
            "dslr", "high quality", "film grain",
        ],
        "recommended_tags": [
            "realistic", "natural skin texture",
            "soft lighting", "sharp focus",
            "detailed face", "detailed skin",
        ],
        "negative_prompt": (
            "illustration, painting, drawing, anime, "
            "cartoon, 3d, render, cgi, sketch, "
            "lowres, bad anatomy, bad hands, text, error, "
            "missing fingers, extra digit, fewer digits, "
            "cropped, worst quality, low quality, "
            "normal quality, jpeg artifacts, signature, "
            "watermark, username, blurry, "
            "deformed, disfigured, mutation, ugly, "
            "plastic skin, doll, mannequin, "
            "over-saturated, over-exposed"
        ),
        "description": "実写系モデル (Beautiful Realistic Asians, ChilloutMix等) - フォトリアル特化",
    },
}


# ============================================================
# 自動補完（Enhancer）ルール
# ============================================================
ENHANCEMENT_RULES: dict[str, dict[str, list[str]]] = {
    "lighting": {
        "keywords": [
            "girl", "woman", "boy", "man", "portrait",
            "person", "face", "photo", "realistic",
        ],
        "suggestions": [
            "soft lighting", "natural lighting", "rim lighting",
            "golden hour",
        ],
    },
    "depth_of_field": {
        "keywords": [
            "portrait", "close-up", "face", "upper body",
            "photo", "realistic", "dslr",
        ],
        "suggestions": [
            "depth of field", "bokeh", "blurry background",
        ],
    },
    "detail": {
        "keywords": [
            "girl", "woman", "boy", "man", "character",
            "person",
        ],
        "suggestions": [
            "detailed face", "detailed eyes", "detailed skin",
        ],
    },
    "background_detail": {
        "keywords": [
            "outdoors", "city", "forest", "beach",
            "nature", "landscape",
        ],
        "suggestions": [
            "detailed background", "scenic",
            "beautiful scenery",
        ],
    },
    "atmosphere": {
        "keywords": [
            "fantasy", "magic", "dream", "ethereal",
            "heaven", "goddess",
        ],
        "suggestions": [
            "particles", "sparkles", "glowing",
            "ethereal atmosphere",
        ],
    },
    "photo_realism": {
        "keywords": [
            "photo", "realistic", "raw", "dslr",
            "film", "fujifilm", "canon", "sony",
        ],
        "suggestions": [
            "skin pores", "natural skin texture",
            "subsurface scattering", "film grain",
        ],
    },
}
