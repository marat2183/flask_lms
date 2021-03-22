FROM python:3.9-buster

RUN adduser --disabled-password --gecos '' worker

WORKDIR /home/worker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN python -m venv venv

RUN venv/bin/pip install -v --no-cache-dir -r requirements.txt
RUN venv/bin/pip install --no-cache-dir gunicorn

COPY --chown=worker:worker app app
COPY wsgi.py config.py run.sh ./
RUN chmod a+x run.sh

ENV PYTHONPATH=$PYTHONPATH:/home/worker
ENV PYTHONPATH=$PYTHONPATH:/home/worker/app
ENV FLASK_APP wsgi.py

RUN chown -R worker:worker ./
USER worker

EXPOSE 5000
CMD [ "./venv/bin/gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]