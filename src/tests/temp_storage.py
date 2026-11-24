"""Yhteinen pohja testeille, jotka tarvitsevat väliaikaisen tallennustiedoston."""
import shutil
import tempfile
import unittest
from pathlib import Path

import storage
from main import app

class TempStorageTestCase(unittest.TestCase):
    """Ohjaa tallennuksen väliaikaiseen tiedostoon jokaisen testin ajaksi."""

    def setUp(self):
        """Luo väliaikaisen kansion ja testiasiakkaan."""
        app.config["TESTING"] = True
        self.tmpdir = tempfile.mkdtemp()
        self.original_file = storage.DATA_FILE
        storage.DATA_FILE = Path(self.tmpdir) / "test.json"
        self.client = app.test_client()

    def tearDown(self):
        """Palauttaa alkuperäisen polun ja poistaa väliaikaisen kansion."""
        storage.DATA_FILE = self.original_file
        shutil.rmtree(self.tmpdir)
