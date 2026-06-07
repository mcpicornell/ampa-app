FROM python:3.13-slim

RUN apt-get update && apt-get install -y locales && \
    locale-gen es_ES.UTF-8 && \
    dpkg-reconfigure locales

ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8

WORKDIR /app

COPY . .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
# gunicorn
#CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8008"]
