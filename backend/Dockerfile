FROM python:3.9-slim

RUN apt update
RUN apt install python3-pip -y
RUN apt install libpq-dev -y

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --break-system-packages --use-deprecated=legacy-resolver

ENV FLASK_APP=app
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]