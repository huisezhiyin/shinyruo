from rest_framework.routers import DefaultRouter
from app_ex.work_ex import views

router = DefaultRouter()
router.register(r'lottery', views.LotteryViewSet, base_name="lottery")
router.register(r'lottery_home', views.LotteryHtmlViewSet, base_name="lottery_home")
urlpatterns = router.urls
