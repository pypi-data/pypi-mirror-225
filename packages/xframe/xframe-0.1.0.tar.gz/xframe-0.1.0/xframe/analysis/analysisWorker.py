import logging
import abc
import traceback
import numpy as np

from xframe.analysis.interfaces import CommunicationInterface
from xframe.analysis.interfaces import DatabaseInterface
from xframe.analysis.interfaces import PresenterInterface


log=logging.getLogger('root')


class AnalysisWorker(abc.ABC):
    def __init__(self):
        from xframe.settings import analysis as settings
        from xframe.database import analysis as db
        from xframe.Multiprocessing import comm_module as comm
        self.settings = settings
        self.db = db
        self.comm_module = comm
        
    @abc.abstractclassmethod
    def start_working(self,*argr):
        pass


    
    
