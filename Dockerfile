FROM python:3.10

RUN pip install django~=4.0 djangorestframework
RUN pip install pdbpp

ENTRYPOINT ["bash"]
