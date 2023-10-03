FROM python:3.8.12-slim
LABEL mantainer="Sitt Guruvanich <aekasitt.g@siamintech.co.th> (@aekasitt)"

### Parse Arguments ###
ARG REDIS_URL
ENV REDIS_URL=${REDIS_URL}
ARG WEB_CONCURRENCY
ENV WEB_CONCURRENCY=${WEB_CONCURRENCY:-5}

### Set up Package Manager for Python dependencies ###
WORKDIR /usr/src/app
COPY pyproject.toml /usr/src/app/pyproject.toml
COPY poetry.lock /usr/src/app/poetry.lock
RUN pip install --upgrade pip               \
  && pip install --no-cache-dir poetry      \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev --no-root --remove-untracked

### Get Certificates for HTTP requests ###
RUN apt update \
  && apt install -y --no-install-recommends ca-certificates

### Get pgrep and pkill commands ###
RUN apt install -y --no-install-recommends procps

### Load App sourcecode on to Image ###
ADD . .
### Create Entrypoint and default command ###
RUN mv entrypoint.sh /usr/local/bin/

### Give execution rights to entrypoint script ###
RUN chmod 0744 /usr/local/bin/*

### Expose Webserver Port ###
ENV PORT=8080
EXPOSE 8080
ENTRYPOINT [ "entrypoint.sh" ]