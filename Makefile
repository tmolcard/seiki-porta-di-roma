create-dot-env:
	echo DATA_PATH=\'$(shell pwd)/data\' >> .env
	echo MODEL_ID=default >> .env
	echo SIMULATION_ID=default >> .env
	echo N_SIMULATIONS=100000 >> .env
	echo POSSIBLE_STARTING_FLOOR_LIST=\'["outdoor", "-1"]\' >> .env
	echo MIN_PATH_LENGTH=3 >> .env
	echo MAX_PATH_LENGTH=16 >> .env

setup-local:
	make create-dot-env
	virtualenv .venv
	echo "../../../../" >> .venv/lib/$(shell ls .venv/lib/)/site-packages/local.pth

static-validation:
	flake8 ./sources ./api
	pylint ./sources
	pylint ./api

docker-build-images:
	docker image build . -t perso/my-python-base:0.1 -f ./deployment/docker/python/base.Dockerfile
	docker image build . -t perso/my-python-api:0.1 -f ./deployment/docker/python/api.Dockerfile

docker-compose-up:
	docker-compose -f ./deployment/docker/docker-compose.yaml up

docker-build-up:
	make docker-build-images
	make docker-compose-up