FROM postgres:10.3

ENV POSTGRES_USER="root"
ENV POSTGRES_PASSWORD="test_pw"

COPY create_dbs.sh /docker-entrypoint-initdb.d
