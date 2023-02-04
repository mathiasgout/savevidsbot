FROM python:3.9.13-slim

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /flask_app
COPY . /flask_app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "wsgi:app"]
