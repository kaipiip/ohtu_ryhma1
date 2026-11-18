"""Testit Reference-tietomallille."""
import unittest
from reference import Reference, generate_cite_key


class TestReference(unittest.TestCase):
    """Reference-luokan ja generate_cite_key-funktion testit."""

    def test_reference_is_created_with_given_fields(self):
        """Viite luodaan annetuilla kentillä, ja valinnaiset kentät ovat tyhjiä."""
        ref = Reference("martin2008", "book", ["Robert C. Martin"],
                        "Clean Code", 2008, publisher="Prentice Hall")
        self.assertEqual(ref.title, "Clean Code")
        self.assertEqual(ref.journal, "")

    def test_cite_key_from_first_last_format(self):
        """Avain muodostuu nimestä muodossa Etunimi Sukunimi."""
        self.assertEqual(generate_cite_key(["Anne-Sophie Mayer"], 2025), "mayer2025")

    def test_cite_key_from_last_first_format(self):
        """Avain muodostuu nimestä muodossa Sukunimi, Etunimi."""
        self.assertEqual(generate_cite_key(["Mayer, Anne-Sophie"], 2025), "mayer2025")
