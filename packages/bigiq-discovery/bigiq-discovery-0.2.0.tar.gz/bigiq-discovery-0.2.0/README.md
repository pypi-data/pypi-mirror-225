[![Python application](https://github.com/thenodon/bigiq-discovery//actions/workflows/python-app.yml/badge.svg)](https://github.com/thenodon/bigiq-discovery//actions/workflows/python-app.yml)
[![PyPI version](https://badge.fury.io/py/bigiq-discovery.svg)](https://badge.fury.io/py/bigiq-discovery)

biqiq-discovery a Prometheus service discovery for F5 BigIQ management platform 
------------------------
# Overview
biqiq-discovery is a Prometheus service discovery for F5 devices managed through BigIQ management platform.

# Labels naming (since 0.2.0)
All labels are returned prefixed as `__meta_bigip_`

# Configuration

Example:

```yaml
bigiq:
  host: www.bigiq.io
  port: 443
  username: user
  password: password

```

## Environment variables

- BIGIQ_DISCOVERY_CONFIG - the path to the above config file, default is `./config.yml`
- BIGIQ_DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY - the output directory for the file discovery files used in your Prometheus
configuration. Each adom will have its own file.
- BIGIQ_DISCOVERY_LOG_LEVEL - the log level, default `WARNING`
- BIGIQ_DISCOVERY_LOG_FILE - the log file, default `stdout`
- BIGIQ_DISCOVERY_HOST - the ip to expose the exporter on, default `0.0.0.0` - only applicable if running in server mode
- BIGIQ_DISCOVERY_PORT - the port to expose the exporter on, default `9694`
- BIGIQ_DISCOVERY_BASIC_AUTH_ENABLED - use basic auth if set to anything, default `false`
- BIGIQ_DISCOVERY_BASIC_AUTH_USERNAME - the username 
- BIGIQ_DISCOVERY_BASIC_AUTH_PASSWORD - the password 
- BIGIQ_DISCOVERY_CACHE_TTL - the ttl in seconds to keep the result from Fortimanager in cache, default `60`

# Run 

## File service discovery
```shell
pip install temp-discovery
BIGIQ_DISCOVERY_CONFIG=config.yml
BIGIQ_DISCOVERY_PROMETHEUS_SD_FILE_DIRECTORY=/etc/prometheus/file_sd/fortigate
python -m bigiq_discovery
```

## Http service discovery
```shell
pip install temp-discovery
BIGIQ_DISCOVERY_CONFIG=config.yml
BIGIQ_DISCOVERY_BASIC_AUTH_ENABLED=true
BIGIQ_DISCOVERY_BASIC_AUTH_USERNAME=foo
BIGIQ_DISCOVERY_BASIC_AUTH_PASSWORD=bar
BIGIQ_DISCOVERY_LOG_LEVEL=INFO
python -m temp_discovery --server
```
Test discovery by curl

```shell
curl -ufoo:bar localhost:9694/prometheus-sd-targets
```


# Prometheus job configuration

Example using the discovery with blackbox exporter

```yaml

- job_name: 'f5-cluster-ping'
  metrics_path: /probe
  params:
    module: [icmp]
  http_sd_configs:
    - url: http://localhost:9694/prometheus-sd-targets
      refresh_interval: 60s
      basic_auth:
        username: foo
        password: bar

  relabel_configs:
    - source_labels:
      - __meta_bigip_platform
      action: replace
      target_label: product
    - source_labels:
        - __meta_bigip_version
      action: replace
      target_label: version
    - source_labels:
        - __meta_bigip_clustered
      action: replace
      target_label: clustered
    - source_labels:
        - __meta_bigip_virtual
      action: replace
      target_label: virtual

    - source_labels: [ __address__ ]
      regex: '(.+):.*'
      target_label: __param_target
    - source_labels: [ __param_target ]
      target_label: instance
    - target_label: __address__
      replacement: 'localhost:9115'
    
```


