from rest_framework.routers import DefaultRouter
from app_ex.bulin import views

router = DefaultRouter()
router.register(r'lottery', views.BulinViewSet, base_name="lottery")
urlpatterns = router.urls
