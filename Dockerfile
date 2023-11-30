FROM python:3.9-slim-bullseye

WORKDIR /app/

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3-pip -y

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip3 install -U setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

COPY fatoshistoricos.py .
COPY bot.conf .

CMD ["python3", "-m", "fatoshistoricos"]