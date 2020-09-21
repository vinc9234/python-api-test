#
# Run the api/ app in a container.
#
# Build and run via:
#
#   docker build . --name=store-api:latest
#   docker run -e MONGO_HOST=mongo-server-address store-api:latest
#
FROM python:3.8
RUN  python -m pip install tox
RUN  mkdir /app
COPY . /app
WORKDIR /app
RUN  python -m pip install -rrequirements.txt
ENV  PYTHONPATH=:.
ENTRYPOINT python api

