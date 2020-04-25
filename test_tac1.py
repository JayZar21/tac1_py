
import tempfile
import datetime
from tac1.tac1 import *
import pytest

@pytest.mark.skip(reason="outdated. Tofix")
def test_notebook():
    temp_folder = tempfile.mkdtemp()
    for i in [1, 2, 3]:
        note_path = temp_folder + os.sep + str(i)
        n = Note(note_path, str(i), "A B C D",  "TEST_NOTE")
        n.write()

    nb = Notebook(temp_folder)
    assert "B" in nb.notes["1"].tags
