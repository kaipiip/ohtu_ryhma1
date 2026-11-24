"""testit viitteen lisäämiselle lomakkeella."""
import unittest
import storage

from tests.temp_storage import TempStorageTestCase


class TestAddReferenceForm(TempStorageTestCase):
    """Käyttäjänä voin lisätä viitteen lomakkeella."""

    def test_form_opens(self):
        """Lomakesivu aukeaa ja kentät näkyvät."""
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for field in ("ref-authors", "ref-title", "ref-year"):
            self.assertIn(field, html)

    def test_valid_reference_is_saved(self):
        """Oikein täytetty lomake tallentaa viitteen ja ohjaa etusivulle."""
        response = self.client.post("/submit", data={
            "reference": "book",
            "ref-authors": "Robert C. Martin",
            "ref-title": "Clean Code",
            "ref-year": "2008",
            "ref-publisher": "Prentice Hall",
        })
        self.assertEqual(response.status_code, 302)
        references = storage.load_references()
        self.assertEqual(len(references), 1)
        ref = references[0]
        self.assertEqual(ref.cite_key, "martin2008")
        self.assertEqual(ref.entry_type, "book")
        self.assertEqual(ref.title, "Clean Code")
        self.assertEqual(ref.year, 2008)
        self.assertEqual(ref.publisher, "Prentice Hall")

    def test_missing_author_is_rejected(self):
        """Ilman kirjoittajaa viitettä ei tallenneta."""
        response = self.client.post("/submit", data={
            "reference": "book",
            "ref-authors": "",
            "ref-title": "Clean Code",
            "ref-year": "2008",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(storage.load_references()), 0)

    def test_missing_title_is_rejected(self):
        """Ilman otsikkoa viitettä ei tallenneta."""
        response = self.client.post("/submit", data={
            "reference": "book",
            "ref-authors": "Robert C. Martin",
            "ref-title": "",
            "ref-year": "2008",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(storage.load_references()), 0)

    def test_invalid_year_is_rejected(self):
        """Vuosi, joka ei ole kokonaisluku, estää tallennuksen."""
        response = self.client.post("/submit", data={
            "reference": "book",
            "ref-authors": "Robert C. Martin",
            "ref-title": "Clean Code",
            "ref-year": "abcd",
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(storage.load_references()), 0)


if __name__ == "__main__":
    unittest.main()
