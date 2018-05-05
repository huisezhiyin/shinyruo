from django.conf.urls import include, url
from django.urls import path
from app_ex.work_ex import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.hello),
    path('admin/', admin.site.urls),
]
