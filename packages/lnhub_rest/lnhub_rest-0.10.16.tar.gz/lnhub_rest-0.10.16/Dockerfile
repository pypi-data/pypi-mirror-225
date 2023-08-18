FROM --platform=linux/amd64 python:3.9
WORKDIR /lnhub-rest
COPY . /lnhub-rest
RUN pip install ./lamindb-setup
RUN pip install --upgrade .[server]
ENTRYPOINT ./scripts/run.sh
