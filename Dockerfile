FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /webapp

COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY . /webapp

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]