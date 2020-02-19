import sys
import os
import npyscreen
from configparser import ConfigParser

DEFAULT_DATA_PATH = "~/.tac1"

NOTE_CONTENT_TPL = \
"""
[title]: {TITLE}
[tags]: {TAG_LIST}

{CONTENT}
"""

class TempDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

def format_tpl(tpl, data):
    return tpl.format_map(TempDict(**data))

class Notebook():

    def __init__(self, path=DEFAULT_DATA_PATH):
        self.notes = dict()
        os.makedirs(path,exist_ok=True)
        for root, dirs, files in os.walk(path):
            for file in files:
                note_path = root + os.sep + file
                n = Note(note_path)
                self.notes[n.title] = n
        print(self.notes)
                

class Note():
    """
    [title]: The title of the note
    [tags]: tag1 tag2

    The content of the note
    """

    NOTE_CONTENT_TPL = \
    """
    [title]: {TITLE}
    [tags]: {TAG_LIST}

    {CONTENT}
    """

    def __init__(self, path):
        self.title = ""
        self.tags = list()
        self.content = ""
        with open(path, "r") as fr:
            content = fr.read()
            if len(content) > 2:
                self.title = content[0].replace("[title]: ", "")
                self.tags = content[1].replace("[tags]: ", "").split(" ")
                self.content = content[2:]

    @classmethod
    def format_note(cls, title, tag_list, content):
        params = \
        {
            "TITLE" : title,
            "TAG_LIST" : tag_list,
            "CONTENT" : content,
        }
        return format_tpl(NOTE_CONTENT_TPL, params)


class TacApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        #self.myDatabase = AddressDatabase()
        self.addForm("MAIN", MainForm)
        #self.addForm("EDITRECORDFM", EditRecord)

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "Hellow World!" )

    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == '__main__':
    app = TacApplication()
    app.run()
