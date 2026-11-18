from dataclasses import dataclass

ENTRY_TYPES = ("article", "book", "inproceedings", "misc")


def parse_authors(text: str) -> list[str]:
    """Muuttaa puolipisteillä erotellun tekstin tekijälistaksi.

    "Mayer, Anne-Sophie; Baygi, Reza M." -> ["Mayer, Anne-Sophie", "Baygi, Reza M."]
    """
    return [name.strip() for name in text.split(";") if name.strip()]


def generate_cite_key(authors: list[str], year: int) -> str:
    """Muodostaa viiteavaimen ensimmäisen tekijän sukunimestä ja vuodesta.

    ["Anne-Sophie Mayer"], 2025 -> "mayer2025"
    ["Mayer, Anne-Sophie"], 2025 -> "mayer2025"
    """
    first = authors[0]
    if "," in first:
        surname = first.split(",")[0]
    else:
        surname = first.split()[-1]
    return f"{surname.strip().lower()}{year}"


@dataclass
class Reference:
    cite_key: str
    entry_type: str
    author: list[str]
    title: str
    year: int
    month: str = ""
    journal: str = ""
    booktitle: str = ""
    publisher: str = ""
    volume: str = ""
    number: str = ""
    pages: str = ""
    doi: str = ""
    url: str = ""