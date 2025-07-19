FROM python:3

RUN groupadd --gid 1000 filer \
    && useradd --uid 1000 --gid 1000 -m filer

RUN mkdir /var/static
RUN mkdir /uploads

RUN pip install flask werkzeug

COPY main.py /var/static/main.py

RUN chown -R filer:filer /var/static
RUN chown -R filer:filer /uploads

EXPOSE 5000

USER filer

CMD python /var/static/main.py
