FROM centos:7

#COPY requirements.txt

RUN yum -y install python3 python3-pip \
    && pip3 install flask gunicorn flask_sqlalchemy psycopg2-binary pymemcache redis \
    && mkdir -p /python/app/templates \
    && mkdir -p /python/app/static/{images,css}

WORKDIR /python/app/

COPY myapp.py /python/app/

COPY myapp.wsgi /python/app/
COPY static/images/* /python/app/static/images/
COPY templates/* /python/app/templates/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=2", "myapp:app"]
