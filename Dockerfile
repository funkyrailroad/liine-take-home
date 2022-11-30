FROM python:3.10

RUN pip install django~=4.0 djangorestframework
RUN pip install pdbpp
RUN pip install psycopg2

ENV DB_HOST=localhost
ENV DB_NAME=liine
ENV DB_PASSWORD=takehome
ENV DB_PORT=5432
ENV DB_USER=postgres

ENTRYPOINT ["bash"]
