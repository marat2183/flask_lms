FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/

RUN pip install --upgrade pip
COPY requirements.txt /var/www/requirements.txt
COPY . /var/www/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

EXPOSE 5000

RUN ["chmod", "a+x", "./run.sh"]
ENTRYPOINT ["./run.sh"]
#CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]