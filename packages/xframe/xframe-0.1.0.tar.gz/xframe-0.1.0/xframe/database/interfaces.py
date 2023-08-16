import abc
import logging
log=logging.getLogger('root')
from xframe.interfaces import DependencyInterfaceTemplate

class HDF5Interface(DependencyInterfaceTemplate):
    @abc.abstractmethod
    def save(path,data: dict):
        log.error('HDF5 dependency not injected. Is h5py python package installed ?')
    @abc.abstractmethod
    def load(path):
        log.error('HDF5 dependency not injected. Is h5py python package installed ?')
    
class YAMLInterface(DependencyInterfaceTemplate):
    @abc.abstractmethod
    def save(path,data: dict):
        log.error('YAML dependency not injected. Is the ruamel python package installed ? ')
    @abc.abstractmethod
    def load(path):
        log.error('YAML dependency not injected. Is the ruamel python package installed ?')

class VTKInterface(DependencyInterfaceTemplate):
    @abc.abstractmethod
    def save(datasets, grid, file_path,dset_names = 'data', grid_type='cartesian'):
        log.error('VTK dependency not injected. Is the vtk package installed ')
    @abc.abstractmethod
    def load(path):
        log.error('VTK dependency not injected. Is the vtk python package installed ?')

class PDBInterface(DependencyInterfaceTemplate):
    @abc.abstractmethod
    def load(pdb_id : str):
        log.error('PDB dependency not injected. Is the pdb_eda python package installed ? ')
    @abc.abstractmethod
    def save(path,data):
        log.error('PDB dependency not injected. Is the pdb_eda python package installed ?')

class OpenCVInterface(DependencyInterfaceTemplate):
    @abc.abstractmethod
    def load(path):
        log.error('OpenCV dependency not injected. Is the opencv-python python package installed ? ')
    @abc.abstractmethod
    def save(path,data):
        log.error('OpenCV dependency not injected. Is the opencv-python python package installed ?')
