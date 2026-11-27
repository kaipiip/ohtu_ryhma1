"""Viitteiden muuntaminen BibTeX-muotoon."""

from reference import Reference


def to_bibtex(ref: Reference) -> str:
    """Muuntaa yhden viitteen BibTeX-merkinnäksi."""
    fields = {
        "author": " and ".join(ref.author),
        "title": ref.title,
        "year": ref.year,
        "month": ref.month,
        "journal": ref.journal,
        "booktitle": ref.booktitle,
        "publisher": ref.publisher,
        "address": ref.address,
        "volume": ref.volume,
        "number": ref.number,
        "pages": ref.pages,
        "doi": ref.doi,
        "url": ref.url,
    }
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields.items() if v)
    return f"@{ref.entry_type}{{{ref.cite_key},\n{body}\n}}"


def references_to_bibtex(references: list[Reference]) -> str:
    """Muuntaa kaikki viitteet yhdeksi BibTeX-tekstiksi."""
    return "\n\n".join(to_bibtex(r) for r in references) + "\n"
