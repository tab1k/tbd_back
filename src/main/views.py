from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import translation
from .models import Logo, News, Video, Team, Case
from .serializers import *

class BaseAPIView(APIView):
    """Базовый класс для обработки языка"""
    
    def get_serializer_context(self):
        """Добавляем язык в контекст сериализатора"""
        context = {}
        language = self.request.GET.get('lang', 'ru')
        
        # Активируем язык для этого запроса
        translation.activate(language)
        self.request.LANGUAGE_CODE = language
        
        context['request'] = self.request
        return context

class LogoAPIView(APIView):
    def get(self, request):
        logo = Logo.objects.all()
        logo_serializer = LogoSerializer(logo, many=True)
        return Response(logo_serializer.data)

class TeamAPIView(BaseAPIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer_context = self.get_serializer_context()
        team_serializer = TeamSerializer(teams, many=True, context=serializer_context)
        return Response(team_serializer.data)

class NewsAPIView(BaseAPIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5

        news = News.objects.all().order_by('-created_at')
        result_news = paginator.paginate_queryset(news, request)
        
        serializer_context = self.get_serializer_context()
        news_serializer = NewsSerializer(result_news, many=True, context=serializer_context)
        
        return paginator.get_paginated_response(news_serializer.data)

class VideoAPIView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5 

        videos = Video.objects.all()
        result_videos = paginator.paginate_queryset(videos, request)
        video_serializer = VideoSerializer(result_videos, many=True)
        return paginator.get_paginated_response(video_serializer.data)

class CaseAPIView(BaseAPIView):
    def get(self, request):
        cases = Case.objects.all().prefetch_related('images')
        serializer_context = self.get_serializer_context()
        case_serializer = CaseSerializer(cases, many=True, context=serializer_context)
        return Response(case_serializer.data)

# Дополнительная вьюшка для конфигурации сайта
class SiteConfigAPIView(BaseAPIView):
    def get(self, request):
        language = request.GET.get('lang', 'ru')
        
        # Получаем основные данные
        main_logo = Logo.objects.first()
        team_count = Team.objects.count()
        news_count = News.objects.count()
        cases_count = Case.objects.count()
        
        serializer_context = self.get_serializer_context()
        
        config_data = {
            'language': language,
            'available_languages': [
                {'code': 'ru', 'name': 'Русский'},
                {'code': 'en', 'name': 'English'}
            ],
            'logo': LogoSerializer(main_logo, context=serializer_context).data if main_logo else None,
            'stats': {
                'team_members': team_count,
                'news_count': news_count,
                'cases_count': cases_count,
            }
        }
        
        return Response(config_data)