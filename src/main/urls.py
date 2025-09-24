from django.urls import path
from .views import LogoAPIView, TeamAPIView, NewsAPIView, VideoAPIView, CaseAPIView

app_name = 'main'

urlpatterns = [
    path('home/logo/', LogoAPIView.as_view(), name='logo'),
    path('home/team/', TeamAPIView.as_view(), name='team'),
    path('home/news/', NewsAPIView.as_view(), name='news'),
    path('home/videos/', VideoAPIView.as_view(), name='videos'),
    path('home/cases/', CaseAPIView.as_view(), name='cases'),
]
