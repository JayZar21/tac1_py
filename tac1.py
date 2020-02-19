import sys
import os
import npyscreen
from configparser import ConfigParser


class TacApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = AddressDatabase()
        self.addForm("MAIN", MainForm)
        self.addForm("EDITRECORDFM", EditRecord)

class MainForm(npyscreen.Form):
    def create(self):
        self.add(npyscreen.TitleText, name = "Text:", value= "Hellow World!" )

    def afterEditing(self):
        self.parentApp.setNextForm(None)

if __name__ == '__main__':
    app = TacApplication()
    app.run()
