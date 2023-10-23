FROM python:3.9.18-slim
LABEL mantainer="Sitt Guruvanich <aekazitt+github@gmail.com> (@aekasitt)"

### Parse Arguments ###
ARG WEB_CONCURRENCY
ENV WEB_CONCURRENCY=${WEB_CONCURRENCY:-5}

### Get Certificates for HTTP requests ###
RUN apt update \
  && apt install -y --no-install-recommends ca-certificates

### Add source-code to targeted build ###
WORKDIR /usr/src/app
ADD . .

### Set up Package Manager for Python dependencies ###
RUN pip install --upgrade pip               \
  && pip install --no-cache-dir poetry      \
  && poetry config virtualenvs.create false \
  && poetry install

### Get Certificates for HTTP requests ###
RUN apt update \
  && apt install -y --no-install-recommends ca-certificates

### Get pgrep and pkill commands ###
RUN apt install -y --no-install-recommends procps

### Create Entrypoint and default command ###
RUN mv entrypoint.sh /usr/local/bin/

### Give execution rights to entrypoint script ###
RUN chmod 0744 /usr/local/bin/*

### Expose Webserver Port ###
ENV PORT=8080
EXPOSE 8080
ENTRYPOINT [ "entrypoint.sh" ]