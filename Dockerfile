FROM python:3.6.5-slim
ENV WWW_WEB_DIR="/wwwroot/www"
MAINTAINER grey chen "837364695@qq.com"

COPY ./sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y nginx

COPY ./pip.conf /root/.pip/pip.conf
COPY . ${WWW_WEB_DIR}/

COPY ./entrypoint.sh entrypoint.sh
RUN pip install -r ${WWW_WEB_DIR}/requirements.txt -U && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]