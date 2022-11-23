FROM python:3.10

COPY . ./app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "Main.py", "0.0.0.0", "10001", "5000", "keys/genesisPrivateKey.pem"]