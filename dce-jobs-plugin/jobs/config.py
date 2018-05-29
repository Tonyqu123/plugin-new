import os


DOCKER_HOST = os.getenv('DOCKER_HOST')

CLIENT_CERTIFICATION_PATH = os.getenv('CLIENT_CERTIFICATION_PATH', '/etc/ssl/private/client/client-cert.pem')
CLIENT_PRIVATE_KEY_PATH = os.getenv('CLIENT_PRIVATE_KEY_PATH', '/etc/ssl/private/client/client-key.pem')
CLIENT_CERTIFICATION_CA_PATH = os.getenv('CLIENT_CERTIFICATION_CA_PATH', '/etc/ssl/private/client/ca.pem')
CLIENT_CERT_AUTH_CONFIG = ((CLIENT_CERTIFICATION_PATH, CLIENT_PRIVATE_KEY_PATH), CLIENT_CERTIFICATION_CA_PATH)

DCE_JOBS_PLUGIN_LOG_STORE_PATH = os.getenv('DCE_JOBS_PLUGIN_LOG_STORE_PATH', '/root')
DCE_JOBS_PLUGIN_ETCD_URL = os.getenv('DCE_JOBS_PLUGIN_ETCD_URL', '')


from log import logger
logger.debug('% Docker host: {} %'.format(DOCKER_HOST))
logger.debug('% etcd url: {} %'.format(DCE_JOBS_PLUGIN_ETCD_URL))
