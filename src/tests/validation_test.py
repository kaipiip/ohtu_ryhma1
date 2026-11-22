"""Testit lomakkeen validoinnille."""
import unittest
from datetime import date

from werkzeug.datastructures import MultiDict

from validation import validate_form


def make_form(changes=None):
    """Luo kelvollisen lomakkeen. changes-sanakirja korvaa kenttiä."""
    fields = {
        "ref-title": "Clean Code",
        "ref-authors": "Robert Martin",
        "ref-year": "2008",
    }
    fields.update(changes or {})
    return MultiDict(fields)


class TestValidateForm(unittest.TestCase):
    """Lomakkeen validointi."""

    def test_valid_form_has_no_errors(self):
        """Kelvollinen lomake ei anna virheitä."""
        self.assertEqual(validate_form(make_form()), [])

    def test_empty_title_is_an_error(self):
        """Pelkistä välilyönneistä koostuva otsikko ei kelpaa."""
        errors = validate_form(make_form({"ref-title": "   "}))
        self.assertIn("Otsikko on pakollinen.", errors)

    def test_empty_author_is_an_error(self):
        """Pelkkä tyhjä kirjoittajakenttä ei kelpaa."""
        errors = validate_form(make_form({"ref-authors": "  "}))
        self.assertIn("Vähintään yksi kirjoittaja vaaditaan.", errors)

    def test_empty_extra_author_fields_are_ignored(self):
        """Ylimääräiset tyhjät kirjoittajakentät eivät haittaa."""
        form = make_form()
        form.add("ref-authors", "")
        self.assertEqual(validate_form(form), [])

    def test_empty_year_is_an_error(self):
        """Vuosi on pakollinen."""
        errors = validate_form(make_form({"ref-year": ""}))
        self.assertIn("Vuosi on pakollinen.", errors)

    def test_year_must_be_four_digits(self):
        """Vuoden pitää olla nelinumeroinen luku."""
        for year in ("abc", "99", "20255", "-5", "20.5"):
            with self.subTest(year=year):
                errors = validate_form(make_form({"ref-year": year}))
                self.assertIn("Vuoden pitää olla nelinumeroinen luku, esim. 2025.", errors)

    def test_year_too_far_in_the_future_is_an_error(self):
        """Vuosi saa olla enintään ensi vuosi."""
        max_year = date.today().year + 1
        errors = validate_form(make_form({"ref-year": str(max_year + 1)}))
        self.assertIn(f"Vuoden pitää olla väliltä 1000-{max_year}.", errors)

    def test_year_before_1000_is_an_error(self):
        """Alle 1000 oleva vuosi ei kelpaa."""
        max_year = date.today().year + 1
        errors = validate_form(make_form({"ref-year": "0999"}))
        self.assertIn(f"Vuoden pitää olla väliltä 1000-{max_year}.", errors)

    def test_next_year_is_accepted(self):
        """Ensi vuosi kelpaa."""
        next_year = str(date.today().year + 1)
        self.assertEqual(validate_form(make_form({"ref-year": next_year})), [])

    def test_empty_month_is_accepted(self):
        """Kuukausi on vapaaehtoinen."""
        self.assertEqual(validate_form(make_form({"ref-month": ""})), [])

    def test_valid_months_are_accepted(self):
        """Kuukaudet 1-12 kelpaavat, myös etunollalla."""
        for month in ("1", "03", "12"):
            with self.subTest(month=month):
                self.assertEqual(validate_form(make_form({"ref-month": month})), [])

    def test_invalid_month_is_an_error(self):
        """Muut kuin luvut 1-12 eivät kelpaa."""
        for month in ("0", "13", "abc", "1.5", "-1"):
            with self.subTest(month=month):
                errors = validate_form(make_form({"ref-month": month}))
                self.assertIn("Kuukauden pitää olla luku väliltä 1-12.", errors)

    def test_empty_doi_is_accepted(self):
        """DOI on vapaaehtoinen."""
        self.assertEqual(validate_form(make_form({"ref-doi": ""})), [])

    def test_valid_dois_are_accepted(self):
        """DOI kelpaa pelkkänä tunnisteena tai doi.org-osoitteena."""
        for doi in ("10.1145/2380552.2380613",
                    "https://doi.org/10.1145/2380552.2380613",
                    "doi:10.1000/abc-123"):
            with self.subTest(doi=doi):
                self.assertEqual(validate_form(make_form({"ref-doi": doi})), [])

    def test_invalid_doi_is_an_error(self):
        """Väärän muotoinen DOI ei kelpaa."""
        for doi in ("1", "hello", "2380552.2380613", "10.1/abc", "10.1145/", "10.1145/a b"):
            with self.subTest(doi=doi):
                errors = validate_form(make_form({"ref-doi": doi}))
                self.assertIn("DOI:n pitää olla muotoa 10.1234/esimerkki.", errors)

    def test_all_errors_are_reported_at_once(self):
        """Kaikki virheet palautetaan kerralla, ei vain ensimmäistä."""
        form = make_form({"ref-title": "", "ref-authors": "", "ref-year": "abc",
                          "ref-month": "13", "ref-doi": "x"})
        self.assertEqual(len(validate_form(form)), 5)
