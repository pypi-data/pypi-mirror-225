import logging
import numpy as np
import abc

from xframe.experiment.interfaces import SimulationInterface
from xframe.experiment.interfaces import DetectorInterface
from xframe.experiment.interfaces import DatabaseInterfaceExperiment
from xframe.experiment.interfaces import CommunicationInterface

log=logging.getLogger('root')


class Experiment:    
    def __init__(self,detector='no detector specified',database='no database specified', simulator='no simulator specified',calibrateData=False):
        
        mode=self.selectOperationMode(detector,database,simulator)
        self.mode=mode
        if mode=='simulation':
            self.checkInterfaceComplianceSimulation(simulator)
            self.simulator=simulator
            
            self.getData=simulator.getData
            self.getGeometry=simulator.getGeometry
            self.experimentalSetup=simulator.getExperimentalSetup()
        elif mode=='experiment':        
            self.checkInterfaceComplianceExperiment(detector,database)            
            self.detector=detector
            self.database=database
            
            self.getGeometry=detector.getGeometry                            
            if calibrateData:
                self.getData=self.getDataCalibrated
            else:
                self.getData=database.getData

            self.experimentalSetup=database.getExperimentalSetup()
        else:
            self.getData=self.getEmpty
            self.getGeometry=self.getEmpty
            self.experimentalSetup=self.getEmpty
            log.error('Experiment opperation mode {} not known.'.format(mode))
    
    def selectOperationMode(self,detector,database,simulator):
        mode=''
        if (detector!='no detector specified') & (database!='no database specified'):
            mode='experiment'
        elif simulator!='no simulator specified':
            mode = 'simulation'
        else:
            mode='empty'
        return mode
    
    def getDataCalibrated(self, dataID):
        rawData=database.getData(dataID)
        data=detector.calibrate(rawData)
        return data

    def getEmpty(self,*args,**kwargs):
        return 'Experiment mode={} NO VALUES SPECIFIED'.format(self.mode)

    
    def checkInterfaceComplianceSimulation(self,simulator):
        try:
            assert isinstance(simulator,SimulationInterface)
        except AssertionError:
            log.error('Specified Simulator is not an instance of SimulationInterface')
            
    def checkInterfaceComplianceExperiment(self,detector,database):
        try:
            assert isinstance(detector,DetectorInterface)
        except AssertionError:
            log.error('Specified Detector is not an instance of the DetectorInterface.')
            
        try:
            assert isinstance(database,DatabaseInterfaceExperiment)
        except:
            log.error('Specified Database is not an instance of the DatabaseInterfaceExperiment.')


        
        mode=self.selectOperationMode(detector,database,simulator)
        self.mode=mode
        if mode=='simulation':
            self.checkInterfaceComplianceSimulation(simulator)
            self.simulator=simulator
            
            self.getData=simulator.getData
            self.getGeometry=simulator.getGeometry
            self.experimentalSetup=simulator.getExperimentalSetup()
        elif mode=='experiment':        
            self.checkInterfaceComplianceExperiment(detector,database)            
            self.detector=detector
            self.database=database
            
            self.getGeometry=detector.getGeometry                            
            if calibrateData:
                self.getData=self.getDataCalibrated
            else:
                self.getData=database.getData

            self.experimentalSetup=database.getExperimentalSetup()
        else:
            self.getData=self.getEmpty
            self.getGeometry=self.getEmpty
            self.experimentalSetup=self.getEmpty
            log.error('Experiment opperation mode {} not known.'.format(mode))
            

class ExperimentWorker(abc.ABC):       
    @abc.abstractmethod
    def get_data(self,mode:str,range:dict,data_modifier : object = 'None'):
        pass
    @abc.abstractmethod
    def get_pixel_grid_reciprocal(self,coord_system:str):
        pass
    @abc.abstractmethod
    def start_working(self):
        pass           
    

