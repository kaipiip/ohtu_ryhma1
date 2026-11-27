"""Viitteen tietomalli ja apufunktiot."""
from dataclasses import dataclass

ENTRY_TYPES = ("article", "book", "inproceedings", "misc")


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
class Reference:  # pylint: disable=too-many-instance-attributes
    """Yksi lähdeviite ja sen BibTeX-kentät."""
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
    address: str = ""