FROM centos:7

RUN yum -y install python3 python3-pip \
    && pip3 install flask gunicorn flask_sqlalchemy psycopg2-binary pymemcache \
    && mkdir -p /python/app/templates

WORKDIR /python/app/

COPY myapp.py /python/app/

COPY myapp.wsgi /python/app/

COPY templates/* /python/app/templates/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "myapp:app"]
