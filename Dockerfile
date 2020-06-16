FROM python:3.7

RUN  pip3 install flask gunicorn && \
     mkdir -p /python/app/templates

WORKDIR /python/app/

COPY *.py /python/app/

COPY myapp.wsgi /python/app/

COPY templates/* /python/app/templates/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "myapp:app"]