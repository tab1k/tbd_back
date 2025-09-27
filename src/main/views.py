from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import translation
from .models import Logo, News, Video, Team, Case
from .serializers import *

class BaseAPIView(APIView):
    """Базовый класс для обработки языка"""
    
    def get_language(self, request):
        """Получаем язык из запроса с приоритетами"""
        # Приоритет: параметр запроса > заголовок Accept-Language > по умолчанию русский
        lang = request.GET.get('lang', '')
        if not lang:
            lang = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru').split(',')[0].split('-')[0]
        return lang if lang in ['ru', 'en'] else 'ru'
    
    def get_serializer_context(self):
        """Добавляем язык в контекст сериализатора"""
        context = {}
        language = self.get_language(self.request)
        
        # Активируем язык для этого запроса
        translation.activate(language)
        self.request.LANGUAGE_CODE = language
        
        context['request'] = self.request
        context['language'] = language  # Добавляем язык в контекст для сериализатора
        return context


class LogoAPIView(APIView):
    def get(self, request):
        logo = Logo.objects.all()
        logo_serializer = LogoSerializer(logo, many=True, context={'request': request})
        return Response(logo_serializer.data)
    

class TeamAPIView(BaseAPIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer_context = self.get_serializer_context()
        team_serializer = TeamSerializer(teams, many=True, context=serializer_context)
        return Response({
            'teams': team_serializer.data,
            'language': serializer_context['language'],
            'count': len(team_serializer.data)
        })

class NewsAPIView(BaseAPIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5

        news = News.objects.all().order_by('-created_at')
        result_news = paginator.paginate_queryset(news, request)
        
        serializer_context = self.get_serializer_context()
        news_serializer = NewsSerializer(result_news, many=True, context=serializer_context)
        
        response = paginator.get_paginated_response(news_serializer.data)
        # Добавляем информацию о языке в ответ
        response.data['language'] = serializer_context['language']
        return response


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
        return Response({
            'cases': case_serializer.data,
            'language': serializer_context['language'],
            'count': len(case_serializer.data)
        })

# Дополнительная вьюшка для конфигурации сайта
class SiteConfigAPIView(BaseAPIView):
    def get(self, request):
        language = self.get_language(request)
        serializer_context = self.get_serializer_context()
        
        # Получаем основные данные
        main_logo = Logo.objects.first()
        team_count = Team.objects.count()
        news_count = News.objects.count()
        cases_count = Case.objects.count()
        video_count = Video.objects.count()
        
        # Получаем последние новости и кейсы для превью
        latest_news = News.objects.all().order_by('-created_at')[:3]
        latest_cases = Case.objects.all().order_by('-created_at')[:3]
        
        config_data = {
            'language': language,
            'available_languages': [
                {'code': 'ru', 'name': 'Русский', 'native': 'Russian'},
                {'code': 'en', 'name': 'Английский', 'native': 'English'}
            ],
            'logo': LogoSerializer(main_logo, context=serializer_context).data if main_logo else None,
            'stats': {
                'team_members': team_count,
                'news_count': news_count,
                'cases_count': cases_count,
                'videos_count': video_count,
            },
            'preview': {
                'latest_news': NewsSerializer(latest_news, many=True, context=serializer_context).data,
                'latest_cases': CaseSerializer(latest_cases, many=True, context=serializer_context).data,
            }
        }
        
        return Response(config_data)

# Дополнительная вьюшка для проверки языка
class LanguageAPIView(APIView):
    def get(self, request):
        """Возвращает текущий активный язык"""
        language = request.GET.get('lang', '')
        if not language:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'ru').split(',')[0].split('-')[0]
        
        language = language if language in ['ru', 'en'] else 'ru'
        translation.activate(language)
        
        return Response({
            'current_language': language,
            'supported_languages': ['ru', 'en'],
            'language_name': 'Русский' if language == 'ru' else 'English',
            'language_native': 'Russian' if language == 'ru' else 'English'
        })
    
    def post(self, request):
        """Установка языка через POST запрос"""
        language = request.data.get('language', 'ru')
        if language not in ['ru', 'en']:
            language = 'ru'
        
        translation.activate(language)
        
        return Response({
            'success': True,
            'message': f'Language changed to {language}',
            'current_language': language
        })