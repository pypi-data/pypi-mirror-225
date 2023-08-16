import abc

class CommunicationInterface(abc.ABC):
    @abc.abstractmethod
    def get_data(self):        
        pass
    @abc.abstractmethod
    def get_geometry(self):        
        pass
    @abc.abstractmethod
    def sendResults(self):        
        pass
    @abc.abstractmethod
    def getGatheredResults(self):        
        pass
    @abc.abstractmethod
    def request_mp_evaluation(self,func,**kwargs):
        pass

class RecipeInterface(abc.ABC):
    results : dict   

    @abc.abstractmethod
    def preProcessing(self):
        pass
    @abc.abstractmethod
    def processData(self,data):
        pass
    @abc.abstractmethod
    def processResults(self,results):
        pass
    @abc.abstractmethod
    def postProcessing(self):
        pass

class PresenterInterface(abc.ABC):
    @abc.abstractmethod
    def present(self):
        pass
    @abc.abstractmethod
    def save(self,path):
        pass


class DatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def load(self,analysisType,restultId):
        pass
    @abc.abstractmethod
    def save(self,analysisType,restultId):
        pass
