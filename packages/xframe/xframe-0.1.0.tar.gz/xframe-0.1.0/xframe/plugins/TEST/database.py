import h5py as h5
import numpy as np
import os
from os import path as op
import time
import logging
import traceback
import re
import glob
import vtk
from vtk.util import numpy_support as vtn

from xframe.experiment.interfaces import DatabaseInterfaceExperiment
from xframe.detectors.interfaces import DatabaseInterfaceDetector
from xframe.analysis.interfaces import DatabaseInterface as DatabaseInterfaceAnalysis
from xframe.analysis.interfaces import CommunicationInterface as ComInterfaceAnalysis
from xframe.library.mathLibrary import plane3D
from xframe.library.mathLibrary import spherical_to_cartesian
#from xframe.analysisRecipes import analysisLibrary as aLib
from xframe.library.gridLibrary import GridFactory
from xframe.library.gridLibrary import NestedArray
from xframe.library.gridLibrary import double_first_dimension
from xframe.library.pythonLibrary import getArrayOfArray
from xframe.library.physicsLibrary import ewald_sphere_theta
from xframe.library.physicsLibrary import ewald_sphere_theta_pi

from xframe.database.euxfel import HDF5_DB
from xframe.database.euxfel import default_DB
from xframe.database.euxfel import VTK_saver
from xframe.database.euxfel import PDB_loader
from xframe.presenters.matplolibPresenter import heat2D_multi
from xframe import settings

log=logging.getLogger('root')
        
class Analysis_DB(default_DB,DatabaseInterfaceAnalysis):
    def __init__(self,**folders_files):
        super().__init__(**folders_files)
    
