# perso/my-python-base
FROM python:3.13-alpine

WORKDIR /code

ADD ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN echo "/code" > /usr/local/lib/python3.13/site-packages/code_path.pth

ADD ./sources /code/sources

ENTRYPOINT ["python"]