"""Open the offline visual practice paper in the user's default browser."""
from __future__ import annotations

import sys
import webbrowser
from pathlib import Path


def resource_path(relative: str) -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return root / relative


def main() -> None:
    page = resource_path("presenter/web/index.html")
    if not page.is_file():
        raise FileNotFoundError(f"Practice paper is missing: {page}")
    webbrowser.open(page.as_uri())


if __name__ == "__main__":
    main()
