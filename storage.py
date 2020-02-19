# -*- coding: utf-8 -*-

from collections import OrderedDict
from configparser import ConfigParser
import os

from common_evo.orcs_client import NormalizeKey, DeNormalizeKey
import subprocess
import codecs


class DataStorage(ConfigParser):
    
    def __init__(self, path):
        ConfigParser.__init__(self)
        self.optionxform=str
        self._path = path
        self._something_to_write = False
        if os.path.exists(path):
            with codecs.open(path, "r", "utf-8") as fr:
                self.read_file(fr)

    @property
    def path(self):
        return self._path
       
    def get_all_normalized_data(self):
        return OrderedDict((NormalizeKey(s, o), self.get(s, o)) \
                        for s in self.sections() \
                            for o in self.options(s))
        
    def get_normalized(self, key):
        return self.get(*DeNormalizeKey(key))
    
    def set_normalized(self, key, value):
        section, option = DeNormalizeKey(key)
        if not section in self.sections():
            self.add_section(section)
        self.set(section, option, value)
        self._something_to_write = True
        
    def del_normalized(self, key):
        fields = DeNormalizeKey(key)
        section = fields[0]
        if len(fields) == 1:
            self.remove_section(section)
        else:
            option = fields[1]
            self.remove_option(section, option)
        self._something_to_write = True
        

    def _save(self):
        with codecs.open(self._path, "w", "utf-8") as fw:
            self.write(fw)
        # force disk flush
        subprocess.call("sync", shell=True)

    def save(self):
        if self._something_to_write:
            self._save()
            self._something_to_write = False
            
    def clear(self):
        ConfigParser.clear(self)
        self._something_to_write = True
        self.save()


class DataStorageRack():
    
    def __init__(self, storage_defs=None):
        self._storages = {}
        self.init_storages(storage_defs)
        
    def add_storage(self, name, path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname) # ensure that the folder path exists
        self._storages[name] = DataStorage(path)
        
    def init_storages(self, storage_defs):
        """storage_defs => dict "NAME" : "STORAGE_FULL_PATH" """
        for name, path in storage_defs.items():
            self.add_storage(name, path)
            
    def get_all(self, name):
        return self._storages[name].get_all_normalized_data()
            
    def get(self, name, key):
        return self._storages[name].get_normalized(key)
    
    def delete(self, name, key):
        self._storages[name].del_normalized(key)
    
    def set(self, name, key, value):
        self._storages[name].set_normalized(key, value)
        self._storages[name].save()
        
    def save_all(self):
        for name in self._storages.keys():
            self._storages[name].save()
        
        
        
