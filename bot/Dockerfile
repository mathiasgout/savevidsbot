FROM python:3.9.13-slim

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /bot
COPY . /bot
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]