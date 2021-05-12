FROM python:3.9-buster AS base

RUN adduser --disabled-password --gecos '' worker
WORKDIR /home/worker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /home/worker/requirements.txt

RUN pip install --upgrade pip
RUN pip install -v --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# ADD . /home/worker

COPY --chown=worker:worker . .

ENV FLASK_APP wsgi.py

# RUN chown -R worker:worker ./

USER worker

#########################
# DEBUG
#########################
FROM base AS debug

RUN pip install -v --no-cache-dir debugpy

EXPOSE 5000

EXPOSE 5678
CMD [ "python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000" ]

#########################
# PRODUCTION
#########################
FROM base AS prod

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]