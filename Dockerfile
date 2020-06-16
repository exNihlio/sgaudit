FROM python:3.7

RUN  pip3 install flask gunicorn boto3 && \
     mkdir -p /python/app/templates

WORKDIR /python/app/

COPY aws templates . /python/app/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "myapp:app"]