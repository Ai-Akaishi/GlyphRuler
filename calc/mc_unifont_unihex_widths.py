# mc_unifont_unihex_widths.py
# 使い方:
#   python mc_unifont_unihex_widths.py --unifont-json /path/to/assets/minecraft/font/include/unifont.json \
#                                      --unifont-zip  /path/to/assets/minecraft/font/unifont.zip \
#                                      --out unifont_mc_like_widths.json
#
# 取得先の目安:
#   <version>.jar 内: assets/minecraft/font/include/unifont.json
#                    assets/minecraft/font/unifont.zip
#
# 出力:
#   {
#     "pixel_size": 16,
#     "widths": { "\\u3042": 16, "\\u4E9C": 16, ... },  # 非BMPは "\uXXXX\uXXXX"
#     "stats": { ... }
#   }

import argparse, json, re
from pathlib import Path
from zipfile import ZipFile

HEX_LINE_RE = re.compile(r'^\s*([0-9A-Fa-f]{4,6}):([0-9A-Fa-f]+)\s*$')

def uescape_from_cp(cp: int) -> str:
    if cp <= 0xFFFF:
        return f"\\u{cp:04X}"
    v = cp - 0x10000
    hi = 0xD800 + (v >> 10)
    lo = 0xDC00 + (v & 0x3FF)
    return f"\\u{hi:04X}\\u{lo:04X}"

def load_size_overrides(unifont_json: Path):
    """unifont.json から size_overrides の範囲を読み込んで [(from,to,left,right), ...] を返す"""
    j = json.loads(unifont_json.read_text(encoding="utf-8"))
    ranges = []
    for prov in j.get("providers", []):
        if prov.get("type") == "unihex":
            for ov in prov.get("size_overrides", []):
                f = ov.get("from"); t = ov.get("to")
                left = ov.get("left"); right = ov.get("right")
                if isinstance(f, str) and isinstance(t, str) and isinstance(left, int) and isinstance(right, int):
                    if len(f) == 1 and len(t) == 1:
                        ranges.append((ord(f), ord(t), left, right))
    # 例：ひらがな・カタカナ・CJK拡張A～・統合漢字 → left=0,right=15（=16px固定）
    return ranges

def override_lr_for(cp: int, overrides):
    """該当 cp に size_overrides があれば (left,right) を返し、無ければ None"""
    for a, b, l, r in overrides:
        if a <= cp <= b:
            return (l, r)
    return None

def bits_from_hex(hex_str: str, width_bits: int):
    """hex 文字列を行ごとのビット列（長さ16、各要素は長さ width_bits の '0'/'1' 文字列）にする"""
    total_bits = len(hex_str) * 4
    assert total_bits % 16 == 0, "hex length must be multiple of 16 rows"
    # 幅が 8/16/24/32 のいずれか（23w17a仕様）
    # https://www.minecraft.net/.../minecraft-snapshot-23w17a
    row_bits = width_bits
    rows = []
    # 2^N 桁のゼロ埋めでビット化
    b = bin(int(hex_str, 16))[2:].zfill(total_bits)
    for i in range(16):
        rows.append(b[i*row_bits:(i+1)*row_bits])
    return rows

def auto_trim_width(rows):
    """全16行のビット列から、左右の空列をトリムした見た目幅を返す（空なら0）"""
    h = len(rows)
    w = len(rows[0]) if rows else 0
    if w == 0:
        return 0
    # 各列に1があるかを調べる
    col_has_ink = [False]*w
    for r in rows:
        for x, ch in enumerate(r):
            if ch == '1':
                col_has_ink[x] = True
    # 左端・右端
    try:
        left = col_has_ink.index(True)
        right = w - 1 - col_has_ink[::-1].index(True)
        return right - left + 1
    except ValueError:
        return 0  # どの列もインク無し

def infer_width_from_hex_len(hex_len):
    """HEX 長からセル幅（8/16/24/32）を推定: 16行 * 幅 / 4 = hex_len"""
    for W in (8, 16, 24, 32):
        if 16 * W // 4 == hex_len:
            return W
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--unifont-json", type=Path, required=True, help="assets/minecraft/font/include/unifont.json")
    ap.add_argument("--unifont-zip",  type=Path, required=True, help="assets/minecraft/font/unifont.zip")
    ap.add_argument("--out", type=Path, default=None, help="output json path")
    args = ap.parse_args()

    # size_overrides（例: CJK を 16px 固定など）
    overrides = load_size_overrides(args.unifont_json)

    width_map = {}
    stats = {"read_lines": 0, "kept": 0, "auto_trimmed": 0, "overridden": 0}
    hist = {}

    with ZipFile(args.unifont_zip, "r") as z:
        for zi in z.infolist():
            if not zi.filename.lower().endswith(".hex"):
                continue
            with z.open(zi, "r") as f:
                for raw in f:
                    line = raw.decode("utf-8", "ignore").strip()
                    if not line or line.startswith("#"):
                        continue
                    m = HEX_LINE_RE.match(line)
                    if not m:
                        continue
                    stats["read_lines"] += 1
                    cp_hex, data_hex = m.group(1).upper(), m.group(2).upper()
                    cp = int(cp_hex, 16)
                    if 0xD800 <= cp <= 0xDFFF:
                        continue  # サロゲートは無視

                    cell_w = infer_width_from_hex_len(len(data_hex))
                    if cell_w is None:
                        # 非対応の幅はスキップ
                        continue

                    # 行ごとビット列
                    rows = bits_from_hex(data_hex, cell_w)

                    # size_overrides があればそれを採用（left/right は 0-indexed 列）
                    lr = override_lr_for(cp, overrides)
                    if lr is not None:
                        left, right = lr
                        w = max(0, right - left + 1)
                        stats["overridden"] += 1
                    else:
                        # 仕様通り左右の空列をトリム
                        w = auto_trim_width(rows)
                        stats["auto_trimmed"] += 1

                    width_map[uescape_from_cp(cp)] = int(w)
                    hist[w] = hist.get(w, 0) + 1
                    stats["kept"] += 1

    out = {
        "pixel_size": 16,
        "widths": dict(sorted(width_map.items(), key=lambda kv: kv[0])),
        "stats": {
            **stats,
            "unique_widths": sorted(hist.keys()),
            "widths_histogram": {str(k): v for k, v in sorted(hist.items())}
        }
    }
    out_path = args.out or args.unifont_zip.with_name("unifont_mc_like_widths.json")
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}  (glyphs:{stats['kept']}  overrides:{stats['overridden']}  auto:{stats['auto_trimmed']})")

if __name__ == "__main__":
    main()
