from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Logo, News, Video, Team, Case
from .serializers import LogoSerializer, NewsSerializer, VideoSerializer, TeamSerializer, CaseSerializer

class HomePageAPIView(APIView):
    def get(self, request):
        # Получаем все записи из моделей
        videos = Video.objects.all()
        teams = Team.objects.all()
        cases = Case.objects.all()
        news = News.objects.all()
        logo = Logo.objects.all()

        # Сериализуем данные
        video_serializer = VideoSerializer(videos, many=True)
        team_serializer = TeamSerializer(teams, many=True)
        case_serializer = CaseSerializer(cases, many=True)
        news_serializer = NewsSerializer(news, many=True)
        logo_serializer = LogoSerializer(logo, many=True)

        # Возвращаем данные в формате JSON
        return Response({
            "videos": video_serializer.data,
            "team": team_serializer.data,
            "cases": case_serializer.data,
            "news" : news_serializer.data,
            "logo" : logo_serializer.data
        })
