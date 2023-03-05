FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .

CMD ["gunicorn", "--capture-output", "foodgram.wsgi:application", "--bind", "0:8000" ]