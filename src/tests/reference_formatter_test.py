"""Testit viitteiden listaukselle."""
import unittest

from main import app, references
from reference import Reference
from reference_formatter import format_authors, format_reference


class TestListing(unittest.TestCase):
    """Käyttäjänä voin listata viitteet luettavassa muodossa."""

    def setUp(self):
        """Tyhjentää viitteet ennen jokaista testiä."""
        self.client = app.test_client()
        references.clear()

    def test_one_author(self):
        """Yksi tekijä näytetään sellaisenaan."""
        self.assertEqual(format_authors(["Mayer"]), "Mayer")

    def test_two_authors(self):
        """Kaksi tekijää erotetaan &-merkillä."""
        self.assertEqual(format_authors(["A", "B"]), "A & B")

    def test_book_is_formatted(self):
        """Kirja muotoillaan luettavaksi riviksi."""
        ref = Reference("mayer2025", "book", ["Mayer"], "Generation AI", 2025)
        self.assertEqual(format_reference(ref), "Mayer (2025). Generation AI.")

    def test_empty_list(self):
        """Ilman viitteitä sivulla lukee 'Ei vielä viitteitä.'"""
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Ei vielä viitteitä.", html)

    def test_reference_is_shown(self):
        """Tallennettu viite näkyy sivulla."""
        references.append(Reference("mayer2025", "book", ["Mayer"], "Generation AI", 2025))
        html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Mayer (2025). Generation AI.", html)
