# perso/my-python-api
FROM perso/my-python-base:0.1

WORKDIR /code

COPY ./requirements_api.txt /code/requirements_api.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements_api.txt

COPY ./api /code/api

ENTRYPOINT ["fastapi"]
CMD ["run", "api/main.py", "--port", "80"]