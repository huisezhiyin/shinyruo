from django.conf.urls import include, url
from app_ex.work_ex import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^', include('app_ex.user_ex.urls')),
    url(r'^', include('app_ex.work_ex.urls')),
    url(r'^',include('app_ex.bulin.urls')),
]
