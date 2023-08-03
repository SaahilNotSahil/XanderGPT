FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN playwright install chromium

COPY . .

CMD ["python", "main.py"]
