from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def inventory_tree(folder: str) -> pd.DataFrame:
    base = ROOT / folder
    rows = []
    for path in sorted(base.rglob("*")):
        if path.is_dir() or path.name.lower() == "desktop.ini":
            continue
        stat = path.stat()
        rows.append(
            {
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "size_bytes": stat.st_size,
                "modified": pd.Timestamp(stat.st_mtime, unit="s").isoformat(),
                "extension": path.suffix.lower(),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    for folder in ["data", "scripts"]:
        df = inventory_tree(folder)
        df.to_csv(ROOT / folder / "_file_inventory.csv", index=False)
        print(f"{folder}: {len(df):,} files")


if __name__ == "__main__":
    main()
