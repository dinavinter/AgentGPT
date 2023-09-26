FROM mysql:8.0

ADD setup.sql /docker-entrypoint-initdb.d

COPY wait-for-db.sh /usr/local/bin/
COPY wait-for-db.sh wait-for-db.sh
RUN chmod +x wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh
