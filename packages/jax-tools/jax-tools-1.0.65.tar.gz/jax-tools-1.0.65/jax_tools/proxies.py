# -*- coding: utf-8 -*-
"""
Set proxies for requests
"""
from jax_tools.network_test import check_connectivity


def local_proxies(host='127.0.0.1',port=8080):
    """
    Set proxies for requests
    Returns: proxies or None

    """
    enable_proxy = True
    if not enable_proxy:
        return None
    http_proxy_address = host
    http_proxy_port = port
    if check_connectivity(http_proxy_address, http_proxy_port):
        proxies = {
            'http': 'http://{}:{}'.format(http_proxy_address, http_proxy_port),
            'https': 'http://{}:{}'.format(http_proxy_address, http_proxy_port),
        }
    else:
        proxies = None
    return proxies
