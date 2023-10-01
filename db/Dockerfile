FROM mysql:8.0
# RUN apt-get update && apt-get install -y openssl
# RUN chown mysql: /etc/mysql/mysql.conf.d/

# ADD run_rsa.sh /docker-entrypoint-initdb.d/

ADD setup.sql /docker-entrypoint-initdb.d

COPY wait-for-db.sh /usr/local/bin/
COPY wait-for-db.sh wait-for-db.sh
RUN chmod +x wait-for-db.sh
RUN chmod +x /usr/local/bin/wait-for-db.sh

