FROM python:3.6.5-slim
ENV WWW_WEB_DIR="/wwwroot/www"
MAINTAINER grey chen "837364695@qq.com"
COPY ./pip.conf /root/.pip/pip.conf
COPY . ${WWW_WEB_DIR}/
RUN pip install -r ${WWW_WEB_DIR}/requirements.txt -U
CMD ["python manage.py runserver"]