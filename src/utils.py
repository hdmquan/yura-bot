from pathlib import Path


class PATH:
    root = Path(__file__).parents[1]
    src = root / "src"
    config = root / "config.yaml"
    state = root / ".state.json"
