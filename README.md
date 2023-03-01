# Software Inventory Exporter
This snap runs a simple python http server with [FastAPI](https://fastapi.tiangolo.com/) that serves, hostname, kernel version, apt packages and snaps in json format.

## Deployment
To get the latest stable version of the snap from Snapstore, run:

```shell
sudo snap install software-inventory-exporter --classic
```

To get the latest development version of the snap, build from the source code and install with --dangerous flag:

```shell
make build
sudo snap install software-inventory-exporter.snap --classic --dangerous
```

## Configuration
To configure the snap for your own environment, create a `config.yaml` file in `$SNAP_DATA` (see [Snap Environment Variables](https://snapcraft.io/docs/environment-variables)) directory with the desired entries. By default, `bind_address` and `port` are configured to the values `0.0.0.0` and `8675`, respectively.

The configuration should have the following format:
```yaml
settings:
  bind_address: <IP>
  port: <port>
```

# Usage
After the installation and configuration you should be able to use the API. Check the automatic documentation by accessing `/docs` by accessing:
`http://<IP>:<port>/docs`

From there you will be able to see all endpoint available and try it out.
