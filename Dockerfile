FROM python:3.12.3
LABEL authors="AndreVale69"

RUN mkdir /simulator-automatic-warehouse
WORKDIR /simulator-automatic-warehouse

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
COPY src/ src
COPY run_webpage.py run_webpage.py
COPY configuration/ configuration
COPY resources/ resources

#ENV PYTHONPATH "${PYTHONPATH}:src/.:src/web_app/.:src/sim/."

CMD ["python", "run_webpage.py"]