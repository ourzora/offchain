from typing import Optional

SCHEME_MAP = [
    " X/\\",
    "+-|",
    "/\\",
    "|-/",
    "O|-",
    "\\",
    "#|-+",
    "OO",
    "#",
    "#O",
]


def get_symbol_by_index(index: int) -> Optional[str]:
    if index == 0:
        return None

    # autoglyphs use a one-based index, so we're using a nice helper method
    return SCHEME_MAP[index - 1]
