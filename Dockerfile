FROM python:3.12.2
LABEL authors="AndreVale69"

RUN mkdir /simulator-automatic-warehouse
WORKDIR /simulator-automatic-warehouse

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src/ src
COPY run_webpage.py run_webpage.py
COPY configuration/ configuration
COPY resources/ resources

#ENV PYTHONPATH "${PYTHONPATH}:src/.:src/web_app/.:src/sim/."

#CMD ["python", "src/web_app/index.py"]
CMD ["python", "run_webpage.py"]