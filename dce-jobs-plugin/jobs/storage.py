import logging
import dce_plugin
from multiprocessing import Lock
from functools import wraps


log = logging.getLogger(__name__)
SETUP_CONFIGS = {
    'jobs': []
}

_STORAGE_LOCK = Lock()


def synchronous(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        _STORAGE_LOCK.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            _STORAGE_LOCK.release()
    return decorated


class init_config():
    try:
        sdk = dce_plugin.PluginSDK()
        c = sdk.get_config()
        if not c:
            sdk.set_config(SETUP_CONFIGS)
    except Exception as e:
        log.critical('Init settings failed and exit!', exc_info=True)
        raise e
    else:
        log.info('Init settings success!')


def get_config():
    sdk = dce_plugin.PluginSDK()
    return sdk.get_config()


def set_config(config):
    sdk = dce_plugin.PluginSDK()
    return sdk.set_config(config)
