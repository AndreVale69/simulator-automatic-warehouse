FROM python:3.11.6
LABEL authors="AndreVale69"

ARG WAREHOUSE_CONFIGURATION_FILE_PATH

RUN mkdir /simulator-automatic-warehouse
WORKDIR /simulator-automatic-warehouse

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ src
COPY configuration/ configuration

#WORKDIR src/web_app

ENV WAREHOUSE_CONFIGURATION_FILE_PATH=$WAREHOUSE_CONFIGURATION_FILE_PATH
ENV PYTHONPATH "${PYTHONPATH}:src/.:src/web_app/.:src/sim/."

CMD ["python", "src/web_app/index.py"]