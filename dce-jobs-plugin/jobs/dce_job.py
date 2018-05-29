import json
import logging
import requests
import urlparse
import dce_plugin

log = logging.getLogger(__name__)

sdk = dce_plugin.PluginSDK()
u = urlparse.urlparse(sdk._plugin_storage_url())
plugin_name = u.path.split('/')[3]
plugin_job_api = u._replace(path='/api/plugins-utils/{plugin_name}/jobs'.format(plugin_name=plugin_name)).geturl()


CREATED = 'Created'
RUNNING = 'Running'
SUCCEED = 'Succeed'
FAILED = 'Failed'
CANCELLED = 'Cancelled'
ALL_STATES = {CREATED, RUNNING, SUCCEED, FAILED, CANCELLED}


def create_plugin_job(name, username, state, plugin_target=None, extra_context=None):
    extra_context = extra_context or {}
    if plugin_target:
        extra_context.update(**{'PluginTarget': plugin_target})
    payload = {
        'Name': name,
        'Reason': {
            'UserName': username,
            'Name': username,
            'ObjectType': 'User'
        },
        'State': state,
        'ExtraContext': extra_context
    }
    try:
        r = requests.post(plugin_job_api, data=json.dumps(payload), verify=False,
                          headers={'Content-Type': 'application/json'})
        log.info(r.content)
    except Exception as e:
        log.error(e, exc_info=True)


def get_plugin_jobs():
    try:
        r = requests.get(plugin_job_api)
        return r.json()
    except Exception as e:
        log.error(e, exc_info=True)
        return []