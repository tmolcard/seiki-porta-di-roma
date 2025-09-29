# Ad Portam Ori

## Install env

Local run requirements :

- python >= 3.13
- docker
- docker-compose

### Setup local environment

```sh
make setup-local
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_api.txt
pip install -r requirements_dev.txt
```

## Launch project

```sh
make docker-build-up
```
