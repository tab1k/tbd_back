from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'admin_panel'

router = DefaultRouter()
router.register(r'requests', RequestViewSet)
router.register(r'users', UserViewSet)
router.register(r'cases', CaseViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'news', NewsViewSet)
router.register(r'logo', LogoViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('', AdminPanelPageView.as_view(), name='admin_panel'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls