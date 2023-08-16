#make sure  numpy does not try to multiprocess over xframes multiprocessing
import os
os.environ["MKL_NUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1" 
os.environ["OMP_NUM_THREADS"] = "1" 
os.environ['OPENBLAS_NUM_THREADS'] = "1"

from xframe import startup_routines

startup_routines.import_settings()
startup_routines.setup_logging()

import logging
log = logging.getLogger('root')

startup_routines.startup_imports()
startup_routines.dependency_injection()
dependency_inject_SOFT = startup_routines.dependency_inject_SOFT

startup_routines.setup_default_database()
startup_routines.initialize_attributes()
startup_routines.setup_plugins()

setup_analysis = startup_routines.setup_analysis
setup_experiment = startup_routines.setup_experiment
run = startup_routines.run
        



