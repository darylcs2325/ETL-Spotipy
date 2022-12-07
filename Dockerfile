FROM python:3.8.15
RUN apt-get update && apt-get install -y --no-install-recommends gcc

RUN python -m pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install pipenv
WORKDIR /
COPY ./src /src
COPY Pipfile .
COPY Pipfile.lock .
EXPOSE 8083
RUN pipenv install --system --deploy