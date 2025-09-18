# pip install pillow
from pathlib import Path
import json
from PIL import Image

# ==== 設定 ====
ASSETS_ROOT = Path(r"minecraft")   # 例: .../minecraft-<ver>/assets/minecraft
DEFAULT_JSON = ASSETS_ROOT / "font" / "default.json"
OUT_CSV = Path("glyph_widths.csv")
ALPHA_THRESHOLD = 0  # 0より大きいアルファを「描画あり」とみなす

def resolve_resource(res: str) -> Path:
    """
    "minecraft:font/ascii.png" のようなリソースロケーションを
    実ファイルパス assets/<ns>/textures/<path> に解決する。
    """
    if ":" not in res:
        # 例: "font/ascii.png" のように namespace 省略の場合は minecraft 扱いにする
        ns, path = "minecraft", res
    else:
        ns, path = res.split(":", 1)
    # PNG は textures/ 配下にあるのがルール（font はテクスチャカテゴリ）
    return ASSETS_ROOT.parent / ns / "textures" / path  # assets/minecraft/../minecraft/textures/font/...

def measure_glyph_width(img: Image.Image) -> int:
    """グリフ（セル画像）の実効幅を、完全透明列を左右トリムする形で算出。"""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    px = img.load()
    w, h = img.size

    # 左端探索
    left = None
    for x in range(w):
        if any(px[x, y][3] > ALPHA_THRESHOLD for y in range(h)):
            left = x
            break
    if left is None:
        return 0  # 完全に空

    # 右端探索
    right = None
    for x in range(w - 1, -1, -1):
        if any(px[x, y][3] > ALPHA_THRESHOLD for y in range(h)):
            right = x
            break

    return right - left + 1

def to_json_uescape(ch: str) -> str:
    """1文字 ch を JSON の \\uXXXX(必要なら2連) で返す。"""
    cp = ord(ch)
    # BMP内（含：単独サロゲートもそのまま4桁化）
    if cp <= 0xFFFF:
        return "\\u%04X" % cp
    # 以降はサロゲートペアに分解
    v = cp - 0x10000
    hi = 0xD800 + (v >> 10)
    lo = 0xDC00 + (v & 0x3FF)
    return "\\u%04X\\u%04X" % (hi, lo)

def main():
    with open(DEFAULT_JSON, "r", encoding="utf-8") as f:
        spec = json.load(f)

    rows_out = []
    providers = spec.get("providers", [])
    for prov in providers:
        if prov.get("type") != "bitmap":
            continue

        file_res = prov["file"]  # 例: "minecraft:font/ascii.png"
        ascent = prov.get("ascent")
        explicit_height = prov.get("height")  # 指定される場合あり（ない時は画像高さ/行数から推定）
        chars_rows = prov.get("chars", [])
        if not chars_rows:
            continue

        # 画像を開く
        img_path = resolve_resource(file_res)
        if not img_path.exists():
            print(f"[WARN] image not found: {img_path}")
            continue

        img = Image.open(img_path).convert("RGBA")
        img_w, img_h = img.size

        # グリッドサイズを算出
        rows = len(chars_rows)
        cols = max(len(row) for row in chars_rows)

        # セルサイズ（幅は画像幅/列数、セル高さは height 指定があればそれ、なければ画像高さ/行数）
        if img_w % cols != 0:
            print(f"[WARN] image width {img_w} not divisible by cols {cols} for {img_path.name}")
        cell_w = img_w // cols if cols > 0 else img_w

        if explicit_height is not None:
            cell_h = int(explicit_height)
            # PNG 内で行ごとに縦詰めされている想定の場合、行オフセットは cell_h を用いる
            # ただし PNG の高さと rows*cell_h が一致しない可能性があるため注意
            if rows * cell_h != img_h:
                # ずれていたら画像高さからも試算
                if img_h % rows == 0:
                    cell_h = img_h // rows
        else:
            if img_h % rows != 0:
                print(f"[WARN] image height {img_h} not divisible by rows {rows} for {img_path.name}")
            cell_h = img_h // rows if rows > 0 else img_h

        # 各セルを切り出し＆幅測定
        for r, row in enumerate(chars_rows):
            for c, ch in enumerate(row):
                # 無効セル（NULL相当）はスキップ
                if ch == "\x00":
                    continue
                # セルの矩形
                x0 = c * cell_w
                y0 = r * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                cell = img.crop((x0, y0, x1, y1))

                measured_w = measure_glyph_width(cell)
                # 必要なら +1 の字間（MCは1pxアドバンスを持つ場合がある）を加算したい場合は下を使用
                # advance = measured_w + 1
                advance = measured_w

                rows_out.append({
                    "char": ch,
                    "codepoint": f"U+{ord(ch):04X}",
                    "provider_image": str(img_path),
                    "provider_file": file_res,
                    "cell_w": cell_w,
                    "cell_h": cell_h,
                    "ascent": ascent,
                    "measured_width": measured_w,
                    "suggested_advance": advance,
                    "row": r,
                    "col": c,
                })

    # CSV 出力
    import csv
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()) if rows_out else [])
        if rows_out:
            writer.writeheader()
            writer.writerows(rows_out)

    print(f"done: {OUT_CSV.resolve()} ({len(rows_out)} glyphs)")

    # さっきの main() の最後に追加する形で使える
    OUT_JSON = Path("glyph_widths.json")

    # rows_out から JSON データを作る
    width_map = {}
    for row in rows_out:
        ch = row["char"]
        w = row["measured_width"]
        # JSON のキーは "\uXXXX" の形式で出したい
        # key = "\\u" + format(ord(ch), "04X")
        key = to_json_uescape(ch)      # ←ここだけ置き換え
        width_map[key] = w

    # 保存
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(width_map, f, ensure_ascii=False, indent=2)

    print(f"done: {OUT_JSON.resolve()} ({len(width_map)} entries)")

if __name__ == "__main__":
    main()
