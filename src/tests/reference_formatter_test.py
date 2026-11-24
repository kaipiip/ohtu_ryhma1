"""Testit viitteiden listaukselle."""
import tempfile
from pathlib import Path
from unittest.mock import patch

from reference import Reference
import storage
from reference_formatter import format_authors, format_reference
from tests.temp_storage import TempStorageTestCase


class TestListing(TempStorageTestCase):
    """Käyttäjänä voin listata viitteet luettavassa muodossa."""

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
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(storage, "DATA_FILE", Path(tmp) / "test.json"):
                storage.add_reference(
                    Reference("mayer2025", "book", ["Mayer"], "Generation AI", 2025)
                )
                html = self.client.get("/").get_data(as_text=True)
        self.assertIn("Mayer (2025). Generation AI.", html)
