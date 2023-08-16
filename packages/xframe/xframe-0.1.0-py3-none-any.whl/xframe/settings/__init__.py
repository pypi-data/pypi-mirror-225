import os
import sys
from importlib import util
from . import general
from .tools import DictNamespace
analysis = DictNamespace(settings_will_be_set_once_an_analysis_worker_is_loaded_on_runtime = 'Not happened yet.')
experiment = DictNamespace(settings_will_be_set_once_an_experiment_worker_is_loaded_on_runtime = 'Not happened yet.')

raw_analysis = 'will_be_set_on_runtime'
raw_experiment = 'will_be_set_on_runtime'

# only to make it the same type as the other settings #
gd = {key:general.__getattribute__(key) for key in dict(general.__dict__).keys() if key[0]!="_"}
general = DictNamespace.dict_to_dictnamespace(gd)

if os.path.exists(general.settings_file):
    spec = util.spec_from_file_location('settings_file',general.settings_file)
    general_update = util.module_from_spec(spec)
    spec.loader.exec_module(general_update)
    gd_update = {key:general_update.__getattribute__(key) for key in dict(general_update.__dict__).keys() if key[0]!="_"}
    general.update(gd_update) 
