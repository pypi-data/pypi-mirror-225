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
from typing import Dict, List, Any, Tuple
import ipaddress


def meta_label_name(name: str) -> str:
    return f"{F5Cluster.meta_label_prefix}{name}"


class F5Cluster:
    meta_label_prefix = '__meta_bigip_'

    def __init__(self, hostname: str, group_name: str):
        self.hostname: str = hostname
        self.group_name: str = group_name
        self.address: str = ''
        self.https_port: int = 443
        self.product: str = ''
        self.state: str = ''
        self.edition: str = ''
        self.version: str = ''
        self.virtual: bool = False
        self.clustered: bool = False
        self.licenseexpired: bool = False
        self.discovery_status: str = ''

    def _as_labels(self) -> Dict[str, str]:
        """
        Return what should be labels
        :return:
        """
        labels = {meta_label_name('product'): self.product,
                  meta_label_name('version'): self.version,
                  meta_label_name('clustered'): str(self.clustered).lower(),
                  meta_label_name('virtual'): str(self.virtual).lower()}

        return labels

    def valid(self) -> Tuple[bool, str]:
        """
        Validate the object
        :return:
        """
        return True, ""

    def as_prometheus_file_sd_entry(self) -> Dict[str, Any]:
        return {'targets': [f"{self.hostname}:{self.port}"], 'labels': self._as_labels()}


def f5_cluster_factory(device: Any) -> F5Cluster:

    cluster = F5Cluster(hostname=device['hostname'].strip(), group_name=device['groupName'].strip())
    cluster.address = device['address'].strip()
    cluster.port = device['httpsPort']
    cluster.product = device['product'].strip()
    cluster.state = device['state'].strip()
    cluster.edition = device['edition'].strip()
    cluster.version = device['version'].strip()
    cluster.virtual = device['isVirtual']
    cluster.clustered = device['isClustered']
    cluster.licenseexpired = device['isLicenseExpired']
    if 'discoveryStatus' in device['properties']:
        cluster.discovery_status = device['properties']['discoveryStatus']
    else:
        cluster.discovery_status = 'UNKNOWN'

    return cluster
