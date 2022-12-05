FROM python:3.10-buster

RUN python -m pip install -U pip wheel setuptools

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . /app

CMD ["python", "main.py"]