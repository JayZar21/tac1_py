import sys
import os
import datetime
import npyscreen
from configparser import ConfigParser
from collections import namedtuple

DEFAULT_DATA_PATH = os.path.expanduser("~/.tac1")


class TempDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

def format_tpl(tpl, data):
    return tpl.format_map(TempDict(**data))

class Notebook():

    def __init__(self, path=DEFAULT_DATA_PATH):
        self.notes = dict()
        os.makedirs(path, exist_ok=True)
        for root, dirs, files in os.walk(path):
            for file in files:
                note_path = root + os.sep + file
                n = Note(note_path)
                self.notes[n.title] = n
        print(self.notes.keys())
                

NOTE_CONTENT_TPL = \
"""[title]: {TITLE}
[tags]: {TAG_LIST}
[time]: {TIME}

{CONTENT}
"""
class Note():

    def __init__(self, path):
        self.title = ""
        self.tags = list()
        self.time = ""
        self.content = ""
        print(path)
        with open(path, "r") as fr:
            content = fr.readlines()
            print(content)
            if len(content) > 2:
                self.title = content[0].replace("[title]: ", "").replace("\n", "")
                self.tags = content[1].replace("[tags]: ", "").replace("\n", "").split(" ")
                self.time = content[2].replace("[time]: ", "").replace("\n", "")
                self.content = content[3:]

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

NOTE_BOOK = Notebook()

class TacApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", NotesGrid)

class NotesGrid(npyscreen.Form):
    def create(self):
        # NOT WORKING WELL
        #grid = self.add(npyscreen.GridColTitles, relx = 5, rely=5, col_titles = [''])
        #grid.values = [ (n.time + " | " + n.title,) for n in NOTE_BOOK.notes.values()]

        nb = self.add(npyscreen.BoxTitle, name="Notes:")
        nb.values = [ n.time + " | " + n.title for n in NOTE_BOOK.notes.values()]


    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == '__main__':
    app = TacApplication()
    app.run()
