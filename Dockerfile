FROM python:3.8

RUN apt-get update && apt-get install gcc
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
WORKDIR /application
COPY application /application
COPY cmd.sh /
COPY requirements.txt /
RUN echo $(ls -la / | grep requirements.txt)
RUN pip install -U pip && pip install -U -r /requirements.txt

EXPOSE 9090 9191
USER uwsgi

CMD ["/cmd.sh"]
