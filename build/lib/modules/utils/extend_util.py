from os import listdir, remove
from os.path import isfile, isdir, join
from shutil import rmtree


class ExtendUtil():
    @staticmethod
    def to_path(raw: str):
        if(not ' ' in raw):
            return raw
        return f"\"{raw}\"" 

    @staticmethod
    def replace(raw: str, key_value_pairs: dict[str, str]):
        text: str = raw
        for i in key_value_pairs:
            text = text.replace(i, key_value_pairs[i])        
        return text
    
    @staticmethod
    def del_all_files(path: str):
        for i in listdir(path):
            if(isfile(join(path, i))):
                remove(join(path, i))
            elif(isdir(join(path, i))):
                rmtree(join(path, i))

