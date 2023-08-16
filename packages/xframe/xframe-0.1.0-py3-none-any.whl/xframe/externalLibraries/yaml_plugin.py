from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
import logging

log=logging.getLogger('root')
yaml = YAML()

class YAML_access:
    @staticmethod
    def save(path, data:dict,**kwargs):
        with open(path,'w') as _file:                                
            yaml.dump(data,_file)
    @staticmethod
    def load(path,**kwargs):
        with open(path,'r') as _file:
            data = yaml.load(_file.read())
        if isinstance(data,type(None)):
            data = {}
        return data
