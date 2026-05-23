import re


def create_slug(value: str) -> str:
    s = value.lower()
    # replace non alphanumeric with hyphen
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # collapse hyphens
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s
