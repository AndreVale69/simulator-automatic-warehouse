FROM python:3.12.3-slim
LABEL authors="AndreVale69"

RUN mkdir /simulator-automatic-warehouse
WORKDIR /simulator-automatic-warehouse

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip -r requirements.txt
COPY src/ src
COPY run_simulator.py run_simulator.py
COPY configuration/ configuration
COPY resources/ resources

#ENV PYTHONPATH "${PYTHONPATH}:src/.:src/web_app/.:src/sim/."

CMD ["python", "run_simulator.py"]