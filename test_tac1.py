
import tempfile
import datetime
from tac1 import *



def test_notebook():
    temp_folder = tempfile.mkdtemp()
    for i in [1, 2, 3]:
        note = temp_folder + os.sep + str(i)
        with open(note, "w") as fw:
            fw.write(Note.format_note(str(i), "A B C D", datetime.datetime.now().strftime("%H:%M %B %d, %Y"), "TEST_NOTE"))
    
    nb = Notebook(temp_folder)
    assert "B" in nb.notes["1"].tags
