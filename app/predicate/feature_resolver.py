import re
from typing import Any

INVALID_FEATURE_PATTERN = re.compile(r"(?:^|\.)(?:\d|_)\w*")

def compile_feature(root: Any, feature: str) -> Any:
    if feature == "":
        return root

    if INVALID_FEATURE_PATTERN.search(feature):
        raise ValueError(f"Invalid feature path: '{feature}'")

    try:
        parts = feature.strip(".").split(".")
        value = root
        for part in parts:
            value = getattr(value, part)
        return value
    except AttributeError:
        return None
