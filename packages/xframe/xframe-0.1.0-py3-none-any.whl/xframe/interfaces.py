import abc

def error_message(cls):
    return f'Optional Dependency {cls._dependency_info_[0]} missing. During import of the external Library {cls._dependency_info_[1]} the following error occured:\n {cls._dependency_info_[2]}'

class DependencyMissing(Exception):
    def __init__(self,message=""):
        super().__init__(message)
        self.message = message
        
class DependencyInterfaceTemplateMeta(abc.ABCMeta):
    def _is_optional_dependency_interface(cls):
        return (cls.__mro__[1].__name__=='DependencyInterfaceTemplate')

    def __call__(cls,*args,**kwargs):
        if cls._is_optional_dependency_interface():
            raise DependencyMissing(error_message(cls))
        instance = super().__call__(*args,**kwargs)                
        return instance
    def __getattr__(cls,key):
        if cls._is_optional_dependency_interface():
            raise DependencyMissing(error_message(cls))
        else:
            return super().__getattr__(key,value)
    def __getattribute__(cls,key):
        attr = super().__getattribute__(key)
        if not isinstance(attr,abc.ABCMeta):
            if key[0]!='_':
                if cls._is_optional_dependency_interface():
                    raise DependencyMissing(error_message(cls))             
        return attr
    
class DependencyInterfaceTemplate(abc.ABC,metaclass=DependencyInterfaceTemplateMeta):
    _dependency_info_=('NoDependencyGiven','NoLibraryGiven',"NoErrorRecieved. Is the current abstract class actually used in dependency injection ?")
