from rest_framework.routers import DefaultRouter
from app_ex.user_ex import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name="user")
router.register(r'user_home', views.UserHtmlViewSet, base_name="user_home")
urlpatterns = router.urls
