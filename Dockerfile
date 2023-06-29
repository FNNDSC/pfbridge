#
# Dockerfile for pfdcm.
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build --build-arg UID=$UID -t local/pfbridge .
#
# In the case of a proxy (located at say 10.41.13.4:3128), do:
#
#    export PROXY="http://10.41.13.4:3128"
#    docker build --build-arg http_proxy=${PROXY} --build-arg UID=$UID -t local/pfbridge .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pfbridge
#
# To pass an env var HOST_IP to the container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pfbridge
#
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

LABEL DEVELOPMENT="                                                         \
    docker run --rm -it                                                     \
    -p 33333:33333                                                          \
    -v $PWD/pfbridge:/app:ro  local/pfbridge /start-reload.sh               \
"

ENV DEBIAN_FRONTEND=noninteractive


COPY requirements.txt /tmp/requirements.txt
RUN apt-get update && apt-get -y install gcc python3-dev
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt && rm -v /tmp/requirements.txt
RUN pip install https://github.com/msbrogli/rpudb/archive/master.zip
RUN pip install tzlocal
COPY ./pfbridge /app

ENV PORT=33333
EXPOSE ${PORT}
