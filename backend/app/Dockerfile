FROM python:3.9.13-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# Install & use pipenv
RUN python -m pip install --upgrade pip 
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

CMD ["uvicorn", "wsgi:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]