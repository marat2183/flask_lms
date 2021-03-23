FROM python:3.9-buster

RUN adduser --disabled-password --gecos '' worker
WORKDIR /home/worker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /home/worker

RUN pip install --upgrade pip
RUN pip install -v --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn


COPY --chown=worker:worker . .

ENV FLASK_APP wsgi.py

RUN chown -R worker:worker ./


USER worker

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]