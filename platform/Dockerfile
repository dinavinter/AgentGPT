FROM python:3.11-slim-buster as prod

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  pkg-config \
  gcc \
  ca-certificates \
  pkg-config \
  openjdk-11-jdk \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.4.2

RUN  apt-get update
RUN  apt-get install --reinstall -y build-essential
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install poetry==1.4.2
RUN pip3 wheel --use-pep517 "jpype1 (==1.4.1)"

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  pkg-config \
  && rm -rf /var/lib/apt/lists/*

# Copying actual application
COPY . /app/src/
RUN poetry install --only main

CMD ["/usr/local/bin/python", "-m", "reworkd_platform"]

FROM prod as dev

RUN poetry install
