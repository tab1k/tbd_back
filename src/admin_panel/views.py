from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from main.models import *
from main.serializers import *
from admin_panel.serializers import *
from .models import Requests
from .serializers import *
from main.models import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from main.models import News
from main.serializers import NewsSerializer, NewsCreateUpdateSerializer
from django.utils import timezone
from django.db.models import Count

class AdminPanelPageView(APIView):
    def get(self, request):
        stats = {
            "users" : User.objects.count(),
            "requests": Requests.objects.count(),
            "videos": Video.objects.count(),
            "team_members": Team.objects.count(),
            "cases": Case.objects.count(),
            "news": News.objects.count(),
            "logos": Logo.objects.count()
        }
        return Response(stats)

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Requests.objects.all()
    serializer_class = RequestSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LogoViewSet(viewsets.ModelViewSet):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    
    def get_serializer_class(self):
        # Для создания и обновления
        if self.action in ['create', 'update', 'partial_update']:
            return CaseCreateUpdateSerializer
        
        # Для GET-запросов определяем по URL или другому критерию
        if self.is_admin_request():
            return CaseAdminSerializer
        return CaseSerializer

    def is_admin_request(self):
        """Определяем, является ли запрос админским"""
        # Вариант 1: по пути URL
        if hasattr(self.request, 'path') and '/admin-panel/' in self.request.path:
            return True
        
        # Вариант 2: по заголовку или параметру
        if self.request.query_params.get('admin') == 'true':
            return True
            
        # Вариант 3: для всех запросов из админки (если она отдельно аутентифицирована)
        # return self.request.user.is_staff  # если используете аутентификацию
        
        return False

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        case = serializer.save()
        
        # Возвращаем данные с изображениями - используем правильный сериализатор для ответа
        if self.is_admin_request():
            response_serializer = CaseAdminSerializer(case, context=self.get_serializer_context())
        else:
            response_serializer = CaseSerializer(case, context=self.get_serializer_context())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        case = serializer.save()
        
        # Возвращаем обновленные данные - используем правильный сериализатор
        if self.is_admin_request():
            response_serializer = CaseAdminSerializer(case, context=self.get_serializer_context())
        else:
            response_serializer = CaseSerializer(case, context=self.get_serializer_context())
        return Response(response_serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TeamCreateUpdateSerializer
        
        if self.is_admin_request():
            return TeamAdminSerializer
        return TeamSerializer

    def is_admin_request(self):
        """Определяем, является ли запрос админским"""
        if hasattr(self.request, 'path') and '/admin-panel/' in self.request.path:
            return True
        if self.request.query_params.get('admin') == 'true':
            return True
        return False

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team_member = serializer.save()
        
        # Возвращаем данные с правильным сериализатором
        if self.is_admin_request():
            response_serializer = TeamAdminSerializer(team_member, context=self.get_serializer_context())
        else:
            response_serializer = TeamSerializer(team_member, context=self.get_serializer_context())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        team_member = serializer.save()
        
        # Возвращаем обновленные данные
        if self.is_admin_request():
            response_serializer = TeamAdminSerializer(team_member, context=self.get_serializer_context())
        else:
            response_serializer = TeamSerializer(team_member, context=self.get_serializer_context())
        return Response(response_serializer.data)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NewsCreateUpdateSerializer
        elif self.request.user.is_staff:
            return NewsAdminSerializer
        else:
            return NewsSerializer
    
    def update(self, request, *args, **kwargs):
        # Всегда используем partial=True для обновления
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({
                'access': str(access_token),
            })
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

class RequestView(APIView):
    def get(self, request):
        requests = Requests.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Заявка успешно отправлена!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)