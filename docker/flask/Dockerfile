FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/

RUN pip install --upgrade pip
COPY requirements.txt /var/www/requirements.txt

COPY ../../config.py /var/www/config.py
COPY ../../wsgi.py /var/www/wsgi.py
COPY ../../app /var/www/app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--threads", "2", "--bind", "0.0.0.0:5000", "wsgi:app"]