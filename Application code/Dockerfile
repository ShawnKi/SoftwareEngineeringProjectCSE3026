FROM python:3.8

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app