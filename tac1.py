from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import os
import time
import datetime
from configparser import ConfigParser
from collections import namedtuple

DEFAULT_DATA_PATH = os.path.expanduser("~/.tac1")

DEBUG = True

# global buffering object
_LOG_BUFFER = sys.stdout if not DEBUG else open("tac1.log", 'wb')

def lprint(msg):
    """Print to stout and log into file"""
    if DEBUG:
        _LOG_BUFFER.write((msg + "\n").encode('UTF-8'))
        _LOG_BUFFER.flush()

class TempDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

def format_tpl(tpl, data):
    return tpl.format_map(TempDict(**data))

class Notebook():

    def __init__(self, path=DEFAULT_DATA_PATH):
        self._path = path
        self.current_id = None
        self.notes = dict()
        os.makedirs(path, exist_ok=True)
        for root, dirs, files in os.walk(path):
            for file in files:
                note_path = root + os.sep + file
                n = Note(note_path)
                self.notes[file] = n
        #print(self.notes.keys())

    def new_note(self, title, tags, content):
        file_name = str(time.time())
        note_path = self._path + os.sep + file_name
        note = Note(note_path, title, tags, content)
        note.write()
        self.notes[file_name] = note
        return note

    def set_note(self, file_name, title, tags, content):
        note = self.notes[file_name]
        note.title = title
        note.tags = tags
        note.content = content
        note.write()
        return note

    def get_indexed_note_list(self):
        return [(n.title, k) for k,n in self.notes.items()]

                
NOTE_CONTENT_TPL = \
"""[title]: {TITLE}
[tags]: {TAG_LIST}
[time]: {TIME}

{CONTENT}
"""
class Note():

    def __init__(self, path, 
                    title="", 
                    tags="", 
                    content=""):
        self.title = title
        self.tags = tags
        self.time = ""
        self.content = content
        self._path = path
        #print(self._path)
        if os.path.exists(self._path):
            self.read()

    @classmethod
    def format_note(cls, title, tag_list, time, content):
        params = \
        {
            "TITLE" : title,
            "TAG_LIST" : tag_list,
            "TIME" : time,
            "CONTENT" : content,
        }
        return format_tpl(NOTE_CONTENT_TPL, params)

    def read(self):
        with open(self._path, "r") as fr:
            content = fr.readlines()
            #print(content)
            if len(content) > 2:
                self.title = content[0].replace("[title]: ", "").replace("\n", "")
                self.tags = content[1].replace("[tags]: ", "").replace("\n", "")
                self.time = content[2].replace("[time]: ", "").replace("\n", "")
                self.content = "\n".join(content[3:])

    def write(self):
        self.time = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
        with open(self._path, "w") as fw:
            fw.write(str(self))

    def __str__(self):
        return self.format_note(self.title, self.tags, self.time, self.content)



"""
NOTE_BOOK = Notebook()

class TacApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", NotesGrid)

class NotesGrid(npyscreen.Form):
    def create(self):
        # NOT WORKING WELL
        #grid = self.add(npyscreen.GridColTitles, relx = 5, rely=5, col_titles = [''])
        #grid.values = [ (n.time + " | " + n.title,) for n in NOTE_BOOK.notes.values()]

        nb = self.add(npyscreen.BoxTitle, name="TAC1", editable=True)
        nb.values = [ n.time + " | " + n.title for n in NOTE_BOOK.notes.values()]


    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == '__main__':
    app = TacApplication()
    app.run()"""

#############

"""class ContactModel(object):
    def __init__(self):
        # Current contact when editing.
        self.current_id = None

        # List of dicts, where each dict contains a single contact, containing
        # name, address, phone, email and notes fields.
        self.contacts = []"""


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height,
                                       screen.width,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Note List")
        self.set_theme("monochrome")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            self._model.get_indexed_note_list(),
            name="note",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_indexed_note_list()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Note")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["note"]
        raise NextScene("Edit Note")

    def _delete(self):
        self.save()
        del self._model.notes[self.data["note"]]
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class NoteView(Frame):
    def __init__(self, screen, model):
        super(NoteView, self).__init__(screen,
                                          screen.height,
                                          screen.width,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Note Details",
                                          reduce_cpu=True)
        self.set_theme("monochrome")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Title:", "title"))
        layout.add_widget(Text("Tags:", "tags"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Text:", "content", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(NoteView, self).reset()
        if self._model.current_id is None:
            self.data = \
            {
                "title": "", 
                "tags": "", 
                "content": "",
            }
        else:
            n = self._model.notes[self._model.current_id]
            self.data = \
            {
                "title": n.title, 
                "tags": n.tags, 
                "content": n.content,
            }

    def _ok(self):
        self.save()
        if self._model.current_id is None:
            note = self._model.new_note(self.data["title"], 
                                        self.data["tags"], 
                                        self.data["content"])
        else:
            n = self._model.notes[self._model.current_id]
            n.title = self.data["title"]
            n.tags = self.data["tags"]
            n.content = self.data["content"]
            n.write()
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


def setup(screen, scene):
    scenes = [
        Scene([ListView(screen, the_notebook)], -1, name="Main"),
        Scene([NoteView(screen, the_notebook)], -1, name="Edit Note")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


the_notebook = Notebook()
last_scene = None
while True:
    try:
        Screen.wrapper(setup, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene