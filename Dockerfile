FROM python:3.10

COPY . ./app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "Main.py", "localhost", "10001", "5000", "keys/genesisPrivateKey.pem"]