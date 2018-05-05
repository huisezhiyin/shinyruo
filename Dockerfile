FROM python:3.6.5-slim
ENV WWW_WEB_DIR="/wwwroot/www"
MAINTAINER grey chen "837364695@qq.com"

COPY ./sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx python3-dev build-essential
RUN apt-get install -y --no-install-recommends libmysqlclient-dev

COPY ./requirements.txt ${WWW_WEB_DIR}/
RUN pip install -r ${WWW_WEB_DIR}/requirements.txt -U

COPY ./pip.conf /root/.pip/pip.conf
COPY . ${WWW_WEB_DIR}/

COPY ./entrypoint.sh entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

#docker run -p 80:8000 -d [images id]