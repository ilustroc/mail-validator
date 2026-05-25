import re

import pandas as pd


def clean_document(value: object) -> str:
    """Normalize a document value as an 8-digit text string."""
    if pd.isna(value):
        return ""

    text = str(value).strip()

    if text.endswith(".0"):
        text = text[:-2]

    digits = re.sub(r"\D", "", text)
    return digits.zfill(8) if digits else ""


def clean_email(email: object) -> str:
    """Trim spaces and normalize an email address to lowercase."""
    if pd.isna(email):
        return ""

    return str(email).strip().lower()


def normalize_column_name(column: object) -> str:
    return str(column).strip().upper()
