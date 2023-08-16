import abc


class ExperimentWorkerInterface(abc.ABC):           
    @abc.abstractmethod
    def get_data(self,mode:str,range:dict,data_modifier : object = 'None'):
        pass
    @abc.abstractmethod
    def get_pixel_grid_reciprocal(self,coord_system:str):
        pass
    @abc.abstractmethod
    def start_working(self):
        pass           
    
class CalibratorInterface(abc.ABC):
    @abc.abstractmethod
    def calibration_worker(self,data_generator,out_modifier = False):
        pass
    
class DetectorInterface(abc.ABC):
    @abc.abstractmethod
    def get_geometry(self):
        pass

class DatabaseInterfaceExperiment(abc.ABC):
    @abc.abstractmethod
    def load(self,dataID):
        pass

class DataSourceInterface(abc.ABC):
    @abc.abstractmethod
    def load(self,dataID):
        pass

class SimulationInterface(abc.ABC):
    @abc.abstractmethod
    def getData(self, dataID):
        pass
    @abc.abstractmethod
    def get_geometry(self):
        pass

class CommunicationInterface(abc.ABC):
    @abc.abstractmethod
    def sendData(self,data):
        pass
