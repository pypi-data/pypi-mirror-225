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
import os
from typing import List, Dict, Any

import yaml

from bigiq_discovery.environments import DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY, DISCOVERY_CONFIG
from bigiq_discovery.api import BigIQ
from bigiq_discovery.fmglogging import Log


log = Log(__name__)


def file_service_discovery():
    # Run for as file service discovery
    if not os.getenv(DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY):
        print(f"Env TEMP_PROMETHEUS_SD_FILE_DIRECTORY must be set to a existing directory path")
        exit(1)
    if not os.path.exists(os.getenv(DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY)):
        print(f"Directory {DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY} does not exists")
        exit(1)
    with open(os.getenv(DISCOVERY_CONFIG, 'config.yml'), 'r') as config_file:
        try:
            # Converts yaml document to python object
            config = yaml.safe_load(config_file)

        except yaml.YAMLError as err:
            print(err)

    bigiq = BigIQ(config)
    clusters = bigiq.get_targets()

    prometheus_file_sd: Dict[str, List[Any]] = {}
    for key, clusters in clusters.items():
        for cluster in clusters:

            if key not in prometheus_file_sd:
                prometheus_file_sd[key] = []
            prometheus_file_sd[key].append(cluster.as_prometheus_file_sd_entry())

        # Generate configuration
        with open(f"{os.getenv(DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY)}/{key}.yaml", 'w') as config_file:
            try:
                if key in prometheus_file_sd:
                    yaml.safe_dump(prometheus_file_sd[key], config_file)
            except yaml.YAMLError as err:
                print(err)
