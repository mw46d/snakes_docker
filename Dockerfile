FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

RUN cd static && git clone https://github.com/bensonruan/webcam-easy.git

EXPOSE 8080

CMD ["python", "app.py"]
