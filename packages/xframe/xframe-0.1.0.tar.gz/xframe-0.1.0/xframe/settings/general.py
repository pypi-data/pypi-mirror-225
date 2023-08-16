import os
n_control_workers = 0 #8
max_parallel_processes = 200
RAM = 512*1024**3 # in Byte, This value is only used if psutil is not installed
cache_aware = True
L1_cache = 64 #32 # Cache size in kB
L2_cache = 512 #256 # Cache size in kB
loglevel = 'INFO' #['WARNING','INFO','DEBUG']


print(f'file = {__file__}')
plugin_paths = [
    os.path.abspath(os.path.join(os.path.dirname(__file__),'../plugins/'))+"/",
    "~/.xframe/plugins",
]

ana_db_class_name= 'Analysis_DB'
exp_db_class_name= 'Experiment_DB'
default_ana_worker_name = 'analysisWorker'
default_exp_worker_name = 'experimentWorker'

log_file = os.path.expanduser('~/.xframe/log/log.txt')
settings_file = os.path.expanduser('~/.xframe/settings.py')

default_settings_regexpr = '[-+]?\d*\.*\d+'
settings_version_key = 'settings_version'

load_plugins = 'all' # or list of plugin names

IO= {"folders":
     {"base":"~/.xframe/"},
     "files":
     {
       #  'startup_settings':
       #  {'name':'settings.yaml','folder':'base'}
     }
     }


