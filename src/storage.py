"""Viitteiden tallennus JSON-tiedostoon."""
import json
from dataclasses import asdict
from pathlib import Path

from reference import Reference

DATA_FILE = Path(__file__).resolve().parent.parent / "viitteet.json"

def load_references() -> list[Reference]:
 """Lukee viitteet tiedostosta. Puuttuva tiedosto tarkoittaa tyhjää listaa."""

def save_references(references: list[Reference]) -> None:
    """Kirjoittaa kaikki viitteet tiedostoon."""
    data = [asdict(ref) for ref in references]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_reference(reference: Reference) -> None:
    """Lisää viitteen ja tallentaa."""

