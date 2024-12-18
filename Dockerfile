FROM python:3.12-alpine

WORKDIR /src

COPY . /

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

CMD ["pipenv", "run", "python3", "main.py"]
