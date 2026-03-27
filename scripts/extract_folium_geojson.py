#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def find_json_bounds(text: str, start_at: int) -> tuple[int, int]:
    start = text.find("{", start_at)
    if start < 0:
        raise ValueError("No JSON object start found after marker")

    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return start, i + 1

    raise ValueError("JSON braces were not balanced")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: extract_folium_geojson.py <folium.html> [output.geojson]", file=sys.stderr)
        return 2

    in_path = Path(sys.argv[1]).expanduser().resolve()
    out_path = (
        Path(sys.argv[2]).expanduser().resolve()
        if len(sys.argv) > 2
        else Path("frontend/public/geojson/tambon_flood_probability_polygons.geojson").resolve()
    )

    html = in_path.read_text(encoding="utf-8", errors="replace")
    marker = "_add("
    idx = html.find(marker)
    if idx < 0:
        raise ValueError("Could not locate Folium geo_json add(...) marker")

    a, b = find_json_bounds(html, idx + len(marker))
    payload = json.loads(html[a:b])
    if payload.get("type") != "FeatureCollection":
        payload = {"type": "FeatureCollection", **payload}

    features = payload.get("features")
    if not isinstance(features, list):
        raise ValueError("Extracted payload is not a valid FeatureCollection")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
    os.replace(tmp_path, out_path)

    print(f"Wrote {len(features)} features to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

