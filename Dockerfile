FROM python:3.12.3-slim
LABEL authors="AndreVale69"

RUN mkdir /simulator-automatic-warehouse
WORKDIR /simulator-automatic-warehouse

COPY requirements.txt requirements.txt
COPY web_app-requirements.txt web_app-requirements.txt
RUN pip install --upgrade pip \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
       gcc libc-dev zlib1g-dev \
    && pip install -r requirements.txt -r web_app-requirements.txt \
    && apt-get autoremove --yes gcc libc-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
COPY src/ src
COPY run_webpage.py run_webpage.py
COPY configuration/ configuration
COPY resources/ resources

#ENV PYTHONPATH "${PYTHONPATH}:src/.:src/web_app/.:src/sim/."

CMD ["python", "run_webpage.py"]