"""Lomakkeen tietojen validointi."""
import re
from datetime import date

MIN_YEAR = 1000
YEAR_PATTERN = re.compile(r"[0-9]{4}")
MONTH_PATTERN = re.compile(r"[0-9]{1,2}")
DOI_PATTERN = re.compile(
    r"(?:https?://(?:dx\.)?doi\.org/|doi:)?10\.[0-9]{4,9}/\S+", re.IGNORECASE
)


def validate_year(year):
    """Vuosi on pakollinen nelinumeroinen luku väliltä 1000 - ensi vuosi."""
    if not year:
        return ["Vuosi on pakollinen."]
    if not YEAR_PATTERN.fullmatch(year):
        return ["Vuoden pitää olla nelinumeroinen luku, esim. 2025."]
    max_year = date.today().year + 1
    if not MIN_YEAR <= int(year) <= max_year:
        return [f"Vuoden pitää olla väliltä {MIN_YEAR}-{max_year}."]
    return []


def validate_month(month):
    """Kuukausi on vapaaehtoinen, mutta jos se on annettu, sen pitää olla 1-12."""
    if not month:
        return []
    if not MONTH_PATTERN.fullmatch(month) or not 1 <= int(month) <= 12:
        return ["Kuukauden pitää olla luku väliltä 1-12."]
    return []


def validate_doi(doi):
    """DOI on vapaaehtoinen, mutta jos se on annettu, sen pitää olla oikeaa muotoa."""
    if doi and not DOI_PATTERN.fullmatch(doi):
        return ["DOI:n pitää olla muotoa 10.1234/esimerkki."]
    return []


def validate_form(form):
    """Tarkistaa lisäyslomakkeen tiedot.

    form on request.form -tyyppinen olio. Palauttaa listan virheilmoituksia,
    tyhjä lista tarkoittaa että lomake on kunnossa.
    """
    errors = []

    if not form.get("ref-title", "").strip():
        errors.append("Otsikko on pakollinen.")

    authors = [a.strip() for a in form.getlist("ref-authors") if a.strip()]
    if not authors:
        errors.append("Vähintään yksi kirjoittaja vaaditaan.")

    errors += validate_year(form.get("ref-year", "").strip())
    errors += validate_month(form.get("ref-month", "").strip())
    errors += validate_doi(form.get("ref-doi", "").strip())

    return errors
