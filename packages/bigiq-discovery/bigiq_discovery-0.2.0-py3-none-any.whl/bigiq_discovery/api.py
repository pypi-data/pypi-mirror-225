# -*- coding: utf-8 -*-
"""
    Copyright (C) 2023  Anders Håål

    This file is part of temp-discovery.

    temp-discovery is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    temp-discovery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with temp-discovery.  If not, see <http://www.gnu.org/licenses/>.

"""

import json

from typing import List, Dict, Any

import requests
import urllib3
from f5sdk.bigiq import ManagementClient

from bigiq_discovery.exceptions import DiscoveryException
from bigiq_discovery.f5_cluster import F5Cluster, f5_cluster_factory
from bigiq_discovery.fmglogging import Log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log = Log(__name__)


class BigIQ:
    def __init__(self, config):
        self.username = config.get('bigiq').get('username')
        self.password = config.get('bigiq').get('password')
        self.host = config.get('bigiq').get('host')
        self.port = config.get('bigiq').get('port')

    def get_targets(self) -> Dict[str, List[F5Cluster]]:
        try:
            bigiq = ManagementClient(host=self.host, port=self.port, user=self.username, password=self.password)
            devices = bigiq.make_request('/mgmt/shared/resolver/device-groups/cm-bigip-allBigIpDevices/devices')
        except Exception as err:
            raise DiscoveryException(message="Failed to connect or fetch", exp=err)

        if 'items' not in devices:
            raise DiscoveryException(message="No items returned")
        all_targets = {}
        for item in devices.get('items'):
            f5_cluster = f5_cluster_factory(item)
            if f5_cluster.group_name not in all_targets:
                all_targets[f5_cluster.group_name] = []
            all_targets[f5_cluster.group_name].append(f5_cluster)
        return all_targets
