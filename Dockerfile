FROM python:3.6.5-slim
ENV WWW_WEB_DIR="/wwwroot/www"
MAINTAINER grey chen "837364695@qq.com"

COPY ./sources.list /etc/apt/sources.list
COPY ./pip.conf /root/.pip/pip.conf
COPY . ${WWW_WEB_DIR}/

RUN apt-get update && apt-get install -y nginx
RUN pip install -r ${WWW_WEB_DIR}/requirements.txt -U
RUN cd ${WWW_WEB_DIR}
CMD ["python manage.py runserver"]