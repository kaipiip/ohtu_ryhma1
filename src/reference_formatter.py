"""Viitteen muotoilu lähdeluettelomaiseksi"""
from reference import Reference

def format_authors(authors: list[str]) -> str:
    """Yhdistää tekijät luettavaksi merkkijonoksi.

    ["A"] -> "A"
    ["A", "B"] -> "A & B"
    ["A", "B", "C"] -> "A, B & C"
    """
    names = [a.strip() for a in authors if a.strip()]
    if not names:
        return "Tuntematon tekijä"
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " & " + names[-1]

def _details(ref: Reference) -> str:
    """Viitetyypin mukaiset lisätiedot otsikon perään."""
    if ref.entry_type == "article":
        osat = []
        if ref.journal:
            osat.append(ref.journal)
        if ref.volume:
            numero = f"({ref.number})" if ref.number else ""
            osat.append(f"{ref.volume}{numero}")
        if ref.pages:
            osat.append(format_pages(ref.pages))
        return ", ".join(osat)

    if ref.entry_type == "book":
        return ref.publisher

    if ref.entry_type == "inproceedings":
        if not ref.booktitle:
            return ""
        teksti = f"In {ref.booktitle}"
        if ref.pages:
            teksti += f", {format_pages(ref.pages)}"
        return teksti

    return ""  # misc ja tuntemattomat tyypitd

def format_reference(ref: Reference) -> str:
    """Palauttaa viitteen luettavana rivinä, esim.
    
    Kirjoittajat (vuosi). Otsikko. Lisätiedot.
    """
    teksti = f"{format_authors(ref.author)} ({ref.year}). {ref.title.rstrip('.')}."
    lisat = _details(ref)
    if lisat:
        teksti += f" {lisat}."
    return teksti
