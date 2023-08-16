import abc
from xframe.interfaces import DependencyInterfaceTemplate

class DatabaseInterface(abc.ABC):
    @abc.abstractmethod
    def save(self,name,data,**kwargs):
        pass
    
    @abc.abstractmethod
    def load(self,name,**kwargs):
        pass
    
class SphericalHarmonicTransformInterface(DependencyInterfaceTemplate):
    '''
    Interface for the external library shtns which supplies spherical harmonic transforms
    '''
    @abc.abstractmethod
    def phi(self):
        pass
    @abc.abstractmethod
    def theta(self):
        pass
    @abc.abstractmethod
    def forward_l(self):
        pass
    @abc.abstractmethod
    def forward_m(self):
        pass
    @abc.abstractmethod
    def inverse_m(self):
        pass
    @abc.abstractmethod
    def inverse_l(self):
        pass

class SoftInterface(DependencyInterfaceTemplate):
    '''
    Interface for the external library shtns which supplies spherical harmonic transforms
    '''
    @abc.abstractmethod
    def forward_cmplx(self):
        pass
    @abc.abstractmethod
    def inverse_cmplx(self):
        pass

class DiscreteLegendreTransform_interface(DependencyInterfaceTemplate):
    '''
    Interface for the external library shtns which supplies spherical harmonic transforms
    '''
    @abc.abstractmethod
    def forward():
        pass
    @abc.abstractmethod
    def inverse():
        pass
    
class GSLInterface(DependencyInterfaceTemplate):
    '''
    Interface for the Gnu Scientific Library wraper 
    '''
    @abc.abstractmethod
    def legendre_sphPlm_array(l_max,m_max,xs,return_orders = False,sorted_by_l = False):
        pass
    @abc.abstractmethod
    def bessel_jl(ls,xs):
        pass
    @abc.abstractmethod
    def hyperg_2F1(a,b,c,z):
        pass
        
    #@abc.abstractmethod
    #def fft_halfcomplex_mixedRadix_inverse(data):
    #    pass
    #
    #@abc.abstractmethod
    #def fft_complex_mixedRadix_forward(data):
    #    pass
    #
    #@abc.abstractmethod
    #def fft_complex_mixedRadix_inverse(data):
    #    pass
    #
    #@abc.abstractmethod
    #def besselZero(order, zeroNumber):
    #    pass   
class PeakDetectorInterface(DependencyInterfaceTemplate):
    '''
    Interface for the Gnu Scientific Library wraper 
    '''
    @abc.abstractmethod
    def find_peaks(dim,data):
        raise AssertionError('PeakDetector was not jet dependency injected.')
