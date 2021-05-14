FROM python:3.8-buster AS base

RUN adduser --disabled-password --gecos '' worker

USER worker

WORKDIR /home/worker

COPY --chown=worker:worker requirements.txt requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m venv venv

RUN venv/bin/pip install --upgrade pip setuptools
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
RUN venv/bin/pip install --no-cache-dir gunicorn

COPY --chown=worker:worker app app
COPY --chown=worker:worker config.py wsgi.py run.sh ./

ENV FLASK_APP wsgi.py

EXPOSE 5000

#########################
# DEBUG
#########################
FROM base AS debug

RUN venv/bin/pip install -v --no-cache-dir debugpy
COPY --chown=worker:worker fake.py fake.py

EXPOSE 5678
CMD [ "venv/bin/python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "flask", "run", "--debugger", "-h", "0.0.0.0", "-p", "5000" ]

#########################
# PRODUCTION
#########################
FROM base AS prod

ENTRYPOINT [ "./run.sh" ]