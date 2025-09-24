from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Logo, News, Video, Team, Case
from .serializers import LogoSerializer, NewsSerializer, VideoSerializer, TeamSerializer, CaseSerializer

class LogoAPIView(APIView):
    def get(self, request):
        logo = Logo.objects.all()
        logo_serializer = LogoSerializer(logo, many=True)
        return Response(logo_serializer.data)


class TeamAPIView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        team_serializer = TeamSerializer(teams, many=True)
        return Response(team_serializer.data)


class NewsAPIView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5

        news = News.objects.all()
        result_news = paginator.paginate_queryset(news, request)
        news_serializer = NewsSerializer(result_news, many=True)
        return paginator.get_paginated_response(news_serializer.data)


class VideoAPIView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 5  # количество видео на странице

        videos = Video.objects.all()
        result_videos = paginator.paginate_queryset(videos, request)
        video_serializer = VideoSerializer(result_videos, many=True)
        return paginator.get_paginated_response(video_serializer.data)


class CaseAPIView(APIView):
    def get(self, request):
        cases = Case.objects.all()
        case_serializer = CaseSerializer(cases, many=True)
        return Response(case_serializer.data)
