from xframe.interfaces import DependencyInterfaceTemplate
import abc

#class DependencyInterfaceTemplate:
#    pass

class MatplotlibInterface(DependencyInterfaceTemplate):
    __dependency__='matplotlib'

class MPLToolkitInterface(DependencyInterfaceTemplate):
    __dependency__='matplotlib'

class OpenCVInterface(DependencyInterfaceTemplate):
    __dependency__='cv2 (opencv-python)'
    @abc.abstractmethod
    def get_polar_image(*args,**kwargs):
        pass

