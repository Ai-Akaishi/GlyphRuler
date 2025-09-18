# make_all_surrogates.py
# 使い方: python make_all_surrogates.py [out.json]

import json
import sys
from pathlib import Path

def u(code_unit: int) -> str:
    return f"\\u{code_unit:04X}"

def build_map(start: int, end: int) -> dict:
    # inclusive range
    return {u(cu): 1 for cu in range(start, end + 1)}

def main():
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("surrogates_all.json")

    high = build_map(0xD800, 0xDBFF)  # D8xx..DBxx
    low  = build_map(0xDC00, 0xDFFF)  # DCxx..DFxx

    data = {
        "high": dict(sorted(high.items())),  # {"\\uD800":1, ..., "\\uDBFF":1}
        "low":  dict(sorted(low.items())),   # {"\\uDC00":1, ..., "\\uDFFF":1}
        "stats": {
            "count_high": len(high),  # 1024
            "count_low": len(low)     # 1024
        }
    }

    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} (high:{len(high)} low:{len(low)})")

if __name__ == "__main__":
    main()
