import importlib
import os
import sys
import datetime
import traceback
import xframe
from xframe.interfaces import DependencyInterfaceTemplateMeta

def import_settings():
    import xframe.settings as settings
    xframe.__setattr__('settings',settings)
def setup_logging():
    from xframe.settings import general
    from xframe import log
    log = log.setup_custom_logger('root',general.loglevel)
    globals().update({'log':log})

# xframe modules to load at import 
modules_to_import  = ['Multiprocessing','database','control.Control',['library','lib'],'analysis.analysisWorker','presenters','detectors']
def startup_imports():
    for module in modules_to_import:
        try:
            if isinstance(module,(list,tuple)):
                module_name = 'xframe.'+module[0]
                xframe.__setattr__(module[1], importlib.import_module(module_name))
            else:
                splitted_name = module.split('.')
                module_name = 'xframe.'+module
                if len(splitted_name) > 1:                
                    xframe.__setattr__(splitted_name[-1], importlib.import_module(module_name))
                else:
                    xframe.__setattr__(module,importlib.import_module(module_name))
            #log.info('loaded {}'.format(module))
                    
        except Exception as e:
            traceback.print_exc()
            log.error('Caught exeption while loading {} with content: {}'.format(module_name,e))


            
# External packages to be dependency injected.
# has to be callde after startup_imports
def dependency_injection():
    external_dependencies_to_inject = [
        ##### math stuff #####
        (('gsl_plugin','GSLPlugin','pygsl'),(xframe.lib.math,'gsl'),()),
        (('flt_plugin','LegendreTransform','flt'),(xframe.lib.math,'leg_trf'),()),
        (('shtns_plugin','sh','shtns'),(xframe.lib.math,'shtns'),()),
        (('persistent_homology','PersistentHomologyPlugin','None'),(xframe.lib.math,'PeakDetector'),()),
        ##### multiprocessing & GPU #####
        ('SharedArray',(xframe.lib.python,'sa'),()),
        ('SharedArray',(xframe.Multiprocessing,'sa'),()),
        (('openCL_plugin','OpenClPlugin','pyopencl'),(xframe.Multiprocessing,'openCL_plugin'),()),
        (('psutil_plugin','PsutilPlugin','psutil'),(xframe.Multiprocessing,'psutil_plugin'),()),
        ###### database plugins ######
        (('vtk_plugin','vtkSaver','vtk'),(xframe.database.database,'VTK_saver'),()),
        (('pdb_plugin','ProteinDB','pdb_eda'),(xframe.database.database,'PDB_loader'),()),
        (('hdf5_plugin','HDF5_DB','h5py'),(xframe.database.database,'HDF5_access','as_object'),()),
        (('yaml_plugin','YAML_access','ruamel_yaml'),(xframe.database.database,'YAML_access'),()),
        (('cv_plugin','CV_Plugin','opencv-python'),(xframe.database.database,'OpenCV_access'),()),
        ###### presenter plugins ######
        (('cv_plugin','CV_Plugin','opencv-python'),(xframe.presenters.openCVPresenter,'CV_Plugin'),()),
        (('matplotlib_plugin','matplotlib','matplotlib'),(xframe.presenters.matplotlibPresenter,'matplotlib'),(xframe.presenters.matplotlibPresenter.depencency_injection_hook_mpl,)),
        (('mpl_toolkits_plugin','mpl_toolkits','matplotlib'),(xframe.presenters.matplotlibPresenter,'mpl_toolkits'),(xframe.presenters.matplotlibPresenter.dependency_injection_hook_mpl_toolkits,)),
    ]
    
    ## Failing to import does not generate an error message or raise an error.
    ## If later a routine is called that would require a
    ## depencency it is called against an abstract calss that throws a corresponding not imported error.
    not_injected=[]    
    for import_source ,import_destination,injection_hooks in external_dependencies_to_inject:
        try:
            if isinstance(import_source,(list,tuple)):
                import_name='xframe.externalLibraries.'+ import_source[0]
                tmp = importlib.import_module(import_name)
                dependency = tmp.__getattribute__(import_source[1])                
            else:
                #import_name='xframe.externalLibraries.'+ import_source
                dependency = importlib.import_module(import_source)
            if len(import_destination)==3:
                if import_destination[2]=='as_object':
                    dependency = dependency()
            setattr(import_destination[0],import_destination[1],dependency)
            if len(injection_hooks)>0:
                for hook in injection_hooks:
                    hook()
        except Exception as e:
            log.debug(traceback.format_exc())
            not_injected.append(import_source)
            attr = getattr(import_destination[0],import_destination[1])
            if isinstance(attr,DependencyInterfaceTemplateMeta):
                if isinstance(import_source,(tuple,list)):
                    dependency_name = import_source[-1]
                else:
                    dependency_name = import_source
                attr._dependency_info_=(dependency_name,import_name,e)
    if len(not_injected)>0:
        log.info(f'Could not dependency inject the following optional dependencies:\n {not_injected}')
        

def dependency_inject_SOFT():
    # separate since it uses numba and requires a bit of time to import.
    try:
        from xframe.externalLibraries.soft_plugin import Soft
        xframe.lib.math.Soft=Soft
    except Exception as e:
        log.error(f'loading PySOFT dependency failed with error {e}')

        
def setup_default_database():
    xframe.database.default = xframe.database.database.default_DB(**xframe.settings.general.IO)

def initialize_attributes():
    xframe.analysis_worker = 'Not set. call xframe.setup_analysis'
    xframe.experiment_worker = 'Not set. call xframe.setup_experiment'
    xframe.experiment_detector = 'Not set. call xframe.setup_experiment'
    xframe.experiment_calibrator = 'Not set. call xframe.setup_experiment'
    xframe.controller = xframe.control.Control.Controller()


## look for plugins
def lookup_plugins():
    opt = xframe.settings.general
    #log.info('looking for plugins at {}'.format(opt.plugin_paths))
    plugin_dict = {}
    for path in opt.plugin_paths:
        path = os.path.expanduser(path)
        try:
           plugin_names = next(os.walk(path))[1]
           for name in plugin_names:
               if name[:2]!='__':
                   plugin_dict[name] = os.path.join(path,name+'/')
           sys.path.append(path)
        except StopIteration as e:
            pass
            #log.warning('Plugin path {} not found.'.format(path))
    if len(plugin_dict) == 0:
        log.warning('No xFrame plugins found at {}. Check the general settings plugin path option.'.format(opt.plugin_paths))
        #log.info('plugin_names = {}'.format(plugin_names))
    #log.info(plugin_dict)
    return plugin_dict    

def setup_plugins():
    xframe.known_plugins = lookup_plugins()
    xframe.__setattr__('plugins',importlib.import_module('xframe.plugins'))





def _parse_plugin_name(name,default_worker_name):
    known_plugins = xframe.known_plugins
    names = name.split('.')
    if len(names) == 1:
        plugin_name = names[0]
        worker_name = default_worker_name
    elif len(names) == 2:
        plugin_name, worker_name = names
    else:
        raise AssertionError('Wrong plugin/worker name format. Allowed are "<Plugin_Name>" or "<Plugin_Name>.<Worker_Name>" but "{}" was given.'.format(names))
    if not plugin_name in known_plugins:
        raise AssertionError('Plugin_Name {} was not found at {}. Known plugins are {}'.format(plugin_name,[path + plugin_name for path in xframe.settings.general.plugin_paths],known_plugins))

    plugin_path = known_plugins[plugin_name]
    worker_path = os.path.join(plugin_path,worker_name+'.py')
    if not os.path.exists(worker_path):
        raise AssertionError('Worker {} for Plugin {} was not found at {}'.format(worker_name,plugin_name,worker_path))            
    return plugin_path,plugin_name,worker_name

def _load_db(plugin_name,db_name,opt):
    db_module_pypath= plugin_name + '.database'
    try:      
        db = getattr(importlib.import_module(db_module_pypath),db_name)(**opt)
    except (AttributeError, ModuleNotFoundError) as e:
        log.info(e)
        log.info('Could not find database class {} in plugin {} use default database instead.'.format(db_name,plugin_name))
        db = xframe.database.database.default_DB(**opt)
    return db
   
def setup_analysis(ana_name='plugin.analysis_worker',ana_settings='settings_name'):
    #sys.path.append(opt.plugin_paths)
    settings = xframe.settings
    database = xframe.database
    controller = xframe.controller
    
    ana_settings_name = ana_settings
    if isinstance(ana_name,bool):
        ana_settings = {type:'mock_settings'}
        analysis_sketch = {False,False}
    else:        
        ana_plugin_path,ana_plugin_name,ana_worker_name = _parse_plugin_name(ana_name,settings.general.default_ana_worker_name)
        ana_settings,ana_raw = database.default.load('settings',plugin_path = ana_plugin_path,worker_name = ana_worker_name,settings_file_name=ana_settings,target ='analysis')
        raw_ana_settings = ana_raw.dict()
        settings.analysis = ana_settings
        settings.raw_analysis = raw_ana_settings
        if 'IO' in ana_settings:
            ana_IO_settings=ana_settings.dict().pop('IO')
        else:
            ana_IO_settings = {}
        ana_db = _load_db(ana_plugin_name,settings.general.ana_db_class_name,ana_IO_settings)
        database.analysis = ana_db
        ana_worker = importlib.import_module(ana_plugin_name+'.'+ana_worker_name).Worker()
        #log.info(ana_worker)
        global analysis_worker
        analysis_worker = ana_worker
        #log.info(ana_worker)
        controller.analysis_worker = ana_worker
def setup_experiment(exp_name=False,exp_settings=False):
    settings = xframe.settings
    database = xframe.database
    controller = xframe.controller
    
    exp_settings_name = exp_settings
    if isinstance(exp_name,bool):
        exp_settings = {type:'mock_settings'}
        exp_sketch = False
    else:
        exp_plugin_path,exp_plugin_name,exp_worker_name = _parse_plugin_name(exp_name,settings.general.default_exp_worker_name)
        exp_settings,exp_raw=database.default.load('settings',plugin_path = exp_plugin_path,worker_name = exp_worker_name,settings_file_name=exp_settings,target ='experiment')
        raw_exp_settings = exp_raw.dict()
        settings.experiment = exp_settings
        settings.raw_experiment = raw_exp_settings
        #importlib.import_module('plugins.' + exp_plugin_name+'.'+exp_worker_name).Worker
        if 'IO' in exp_settings:
            exp_IO_settings = exp_settings.dict().pop('IO')
        else:
            exp_IO_settings = {}
        exp_db = _load_db(exp_plugin_name,settings.general.exp_db_class_name,exp_IO_settings)
        database.experiment = exp_db
        try:
            det_opt = exp_settings.get('detector',{})
            det_name = det_opt.get('name','')
            detector =  getattr(importlib.import_module('xframe.detectors.agipd'),det_name)(exp_db,opt = det_opt,load_geometry_file = True)
        except AttributeError as e:
            #log.info(e)
            #traceback.print_exc()
            log.info('Run with default detector.')
            detector = False
        try:
            cal_name = exp_settings['calibrator'].get('name','')
            #log.info('selected calibrator = {}'.format(cal_name))
            calibrator =  getattr(importlib.import_module('xframe.calibrators.calibrators'),cal_name)(exp_db,opt = exp_settings)
        except (AttributeError,KeyError) as e:
            #log.info(e)
            #traceback.print_exc()
            log.info('Run with default calibrator.')
            calibrator = False
        exp_worker = importlib.import_module(exp_plugin_name+'.'+exp_worker_name).Worker(detector = detector,calibrator = calibrator)
        global experiment_worker
        experiment_worker = exp_worker
        controller.experiment_worker = exp_worker



def run(ana_name='plugin.analysis_worker',ana_settings='settings_name',exp_name=False,exp_settings=False, update_workers = True,oneshot = False):
    settings = xframe.settings
    database = xframe.settings
    controller = xframe.controller
    
    if (not isinstance(xframe.analysis_worker,xframe.analysisWorker.AnalysisWorker)) or update_workers:
        #log.info('setting up analysis workers')
        setup_analysis(ana_name=ana_name,ana_settings=ana_settings)
        setup_experiment(exp_name=exp_name,exp_settings=exp_settings)
    
    date_time = str(datetime.datetime.now())
    if settings.analysis.get('save_settings',False):
        database.analysis.save('settings',settings.raw_analysis,path_modifiers={'time':date_time})
        settings.analysis['out_settings_path']=database.analysis.get_path('settings',path_modifiers={'time':date_time,'file_name':settings.analysis.file_name},is_file=False)
    if not isinstance(xframe.experiment_worker,str):
        if settings.experiment.get('save_settings',False):
            database.experiment.save('settings',settings.raw_experiment,path_modifiers={'time':date_time})
            settings.experiment['out_settings_path']=database.experiment.get_path('settings',path_modifiers={'time':date_time,'file_name':settings.experiment.file_name},is_file=False)
        
    result = xframe.lib.python.measureTime(controller.startAnalysis)(oneshot = oneshot)
    return result
 
