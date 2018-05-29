#!/usr/bin/env python

import logging
from docker import APIClient
from docker.tls import TLSConfig

from config import CLIENT_CERT_AUTH_CONFIG


log = logging.getLogger(__name__)
AGENT_CLIENTS = {}


class AgentClient(APIClient):
    pass


def get_agent_client(base_url, version=None, timeout=30):
    global AGENT_CLIENTS
    if base_url not in AGENT_CLIENTS:
        cert, _ = CLIENT_CERT_AUTH_CONFIG

        if not base_url.startswith('https://'):
            base_url = 'https://' + base_url

        version = version or 'auto'
        AGENT_CLIENTS[base_url] = AgentClient(base_url=base_url,
                                              version=version,
                                              timeout=timeout,
                                              tls=TLSConfig(client_cert=cert, verify=False)
                                              )
    return AGENT_CLIENTS[base_url]


if __name__ == '__main__':
    c = get_agent_client('192.168.100.200:12374')
    print c.info()