import traceback
import sys
import xframe
import logging
log = logging.getLogger('root')

plugins_to_load = xframe.settings.general.load_plugins
for plugin_name,plugin_path in xframe.known_plugins.items():
    try:
        if isinstance(plugins_to_load,(list,tuple)):
            if plugin_name in plugins_to_load:
                locals().update({plugin_name:__import__(plugin_name)})
        else:        
            locals().update({plugin_name:__import__(plugin_name)})
    except Exception as e:
        log.error(f'Error during import of plugin at {plugin_path}, Traceback:\n'+traceback.format_exc())

        
