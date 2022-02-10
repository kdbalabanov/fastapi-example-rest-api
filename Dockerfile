# Use an official Python runtime as an image
FROM python:3.9

WORKDIR /fastapi-project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

ENV PYTHONPATH /fastapi-project

EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0"]