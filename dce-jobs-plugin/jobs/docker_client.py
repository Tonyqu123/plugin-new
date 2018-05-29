import os
import logging
from docker import APIClient

from agent_client import get_agent_client
from config import DOCKER_HOST
from const import LABEL_JOB_AGENT_KEY
from const import LABEL_JOB_AGENT_VALUE
from const import LABEL_DCE_PLUGIN_NAME
from const import DCE_PLUGIN_NAME
from const import JOB_AGENT_SERVICE_NAME

# Caution
AGENT_TARGET_PORT = 2376

AGENT_PUBLISHED_PORT = os.getenv('AGENT_PUBLISHED_PORT')
if AGENT_PUBLISHED_PORT and AGENT_PUBLISHED_PORT.isdigit():
    AGENT_PUBLISHED_PORT = int(AGENT_PUBLISHED_PORT)
else:
    AGENT_PUBLISHED_PORT = 12374


log = logging.getLogger(__name__)

# "192.168.1.10": DCEDockerClient()
CACHED_NODE_IP = {}


class DCEDockerClient(APIClient):
    def create_service_raw(self, service_spec, auth_header=None):
        headers = {}
        if auth_header:
            headers['X-Registry-Auth'] = auth_header

        url = self._url('/services/create')
        return self._result(self._post_json(url, data=service_spec, headers=headers), True)

    def update_service_raw(self, service_id, version, service_spec):
        url = self._url('/services/%s/update?version=%s' % (service_id, version))
        return self._result(self._post_json(url, data=service_spec), json=False)


class Node(object):
    def __init__(self, node_id, node_role, node_hostname, addr):
        self.node_id = node_id
        self.node_role = node_role
        self.node_hostname = node_hostname
        self.addr = addr
        self.networks = []

    @classmethod
    def from_data(cls, data):
        addr = data.get('Status', {}).get('Addr')
        if addr in {'127.0.0.1', '0.0.0.0'}:
            addr = data.get('ManagerStatus', {}).get('Addr', '').split(':')[0]

        return cls(
            node_id=data.get('ID'),
            node_role=data.get('Spec', {}).get('Role'),
            node_hostname=data.get('Description', {}).get('Hostname'),
            addr=addr
        )

    def set_networks(self, networks):
        """
        NEVER FORGET set .networks
        """
        for network in networks:
            if network.node.node_id == self.node_id:
                self.networks.append(network)

    def __str__(self):
        return '<NodeID: {0} Name: {1}>'.format(self.node_id[:4], self.node_hostname)


docker_client = DCEDockerClient(base_url=DOCKER_HOST)


def get_global_agent_service():
    try:
        return docker_client.inspect_service(JOB_AGENT_SERVICE_NAME)
    except Exception:
        return {}


def get_nodes_raw():
    """
    return [{}, {}]
    """
    try:
        return docker_client.nodes()
    except Exception as e:
        log.error('Fetch node failed!', exc_info=True)
        return []


def init_global_agent_service():
    global AGENT_TARGET_PORT
    global AGENT_PUBLISHED_PORT
    global docker_client

    agent_service = get_global_agent_service()
    agent_service_image = agent_service.get('Spec', {}).get('TaskTemplate', {}).get('ContainerSpec', {}).get('Image')

    ss = docker_client.services(filters={'label': ['{0}={1}'.format(LABEL_DCE_PLUGIN_NAME, DCE_PLUGIN_NAME)]})
    if not ss:
        log.critical('Init global agent service cannot find self service!')
        raise Exception('self_service_not_found')

    self_service = ss[0]
    self_image = self_service.get('Spec', {}).get('TaskTemplate', {}).get('ContainerSpec', {}).get('Image')

    if agent_service_image == self_image:
        return

    agent_spec = {
            "Name": JOB_AGENT_SERVICE_NAME,
            "Labels": {
                "io.daocloud.dce.system": "dce-jobs-plugin-agent"
            },
            "TaskTemplate": {
                "ContainerSpec": {
                    "Env": [
                    ],
                    "Image": self_image,
                    "Labels": {
                        "io.daocloud.dce.system": "dce-jobs-plugin-agent",
                        LABEL_JOB_AGENT_KEY: LABEL_JOB_AGENT_VALUE
                    },
                    "Command": [
                        "/jobs/agent.sh"
                    ],
                    "Args": [],
                    "Mounts": [
                        {
                            "Type": "bind",
                            "Source": "/var/run/docker.sock",
                            "Target": "/var/run/docker.sock"
                        }
                    ],
                    "DNSConfig": {}
                },
                "Resources": {
                    "Limits": {
                        "MemoryBytes": 1073741824,
                        "NanoCPUs": 500000000
                    }
                },
                "RestartPolicy": {
                    "Condition": "any",
                    "MaxAttempts": 0
                },
                "Placement": {},
                "LogDriver": {
                    "Name": "json-file"
                },
                "ForceUpdate": 0
            },
            "Mode": {
                "Global": {}
            },
            "UpdateConfig": {
                "Parallelism": 1,
                "FailureAction": "pause",
                "MaxFailureRatio": 0
            },
            "EndpointSpec": {
                "Mode": "vip",
                "Ports": [
                    {
                        "TargetPort": AGENT_TARGET_PORT,
                        "PublishedPort": AGENT_PUBLISHED_PORT,
                        "Protocol": "tcp",
                        "PublishMode": "host"
                    }
                ]
            }
        }
    try:
        if agent_service:
            log.info('Update global agent service from {0} to {1}'.format(
                agent_service_image,
                self_image
            ))
            agent_id = agent_service.get('ID')
            agent_index = agent_service.get('Version', {}).get('Index')
            docker_client.update_service_raw(agent_id, agent_index, agent_spec)
        else:
            log.info('Create global agent service with {0}'.format(
                self_image
            ))
            docker_client.create_service_raw(agent_spec)
    except Exception as e:
        log.critical('Init global agent service failed and exit!', exc_info=True)
        raise e
    else:
        log.info('Init global agent service success!')


def get_node_docker_client(node_id):
    """
    node_id -> node.addr -> AgentClient(node.addr)
    """
    if node_id not in CACHED_NODE_IP:
        nodes = [Node.from_data(i) for i in get_nodes_raw()]
        for n in nodes:
            CACHED_NODE_IP[n.node_id] = n.addr

        node = next((n for n in nodes if n.node_id == node_id), None)
        if not node:
            raise Exception('Node with id: {0} not found!'.format(node_id))

    return get_agent_client(CACHED_NODE_IP[node_id] + ':' + str(AGENT_PUBLISHED_PORT))


def exec_create(node_id, container_id, cmd, privileged, user, env):
    client = get_node_docker_client(node_id)
    exec_instance = client.exec_create(container_id, cmd, privileged=privileged, user=user, environment=env)
    return exec_instance


def exec_start(node_id, exec_instance, stream=False):
    if not isinstance(exec_instance, (str, unicode)):
        exec_instance = exec_instance['Id']

    client = get_node_docker_client(node_id)
    output = client.exec_start(exec_instance, stream=stream)
    return output


def exec_inspect(node_id, exec_instance):
    if not isinstance(exec_instance, (str, unicode)):
        exec_instance = exec_instance['Id']

    client = get_node_docker_client(node_id)
    exec_result = client.exec_inspect(exec_instance)
    return exec_result
