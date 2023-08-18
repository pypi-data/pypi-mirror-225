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

from typing import Dict, List

from prometheus_client.registry import Collector, Metric

from bigiq_discovery.metrics import TempMetrics
from bigiq_discovery.f5_cluster import F5Cluster


def to_list(metric_generator) -> List[Metric]:
    metrics = []
    for metric in metric_generator:
        if metric.samples:
            # Only append if the metric has a list of Samples
            metrics.append(metric)
    return metrics


class TempCollector(Collector):

    def __init__(self, fws: Dict[str, List[F5Cluster]]):
        self.fws = fws

    async def collect(self):
        all_module_metrics = []
        transformer = TempMetrics(self.fws)
        transformer.parse()
        t = to_list(transformer.metrics())
        all_module_metrics.extend(t)

        return all_module_metrics
