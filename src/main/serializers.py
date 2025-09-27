from rest_framework import serializers
from .models import CaseImage, Logo, News, Video, Team, Case


class CaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseImage
        fields = ['id', 'image', 'created_at']

class CaseSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    images = CaseImageSerializer(many=True, read_only=True)
    
    def get_title(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'GET'):
            language = request.GET.get('lang', 'ru')
        else:
            language = 'ru'
        return obj.title(language)
    
    def get_description(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'GET'):
            language = request.GET.get('lang', 'ru')
        else:
            language = 'ru'
        return obj.description(language)
    
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'images', 'created_at', 'updated_at', 'translation_status']

# Для админки (все поля)
class CaseAdminSerializer(serializers.ModelSerializer):
    images = CaseImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Case
        fields = ['id', 'title_ru', 'title_en', 'description_ru', 'description_en', 
                 'images', 'created_at', 'updated_at', 'translation_status']


class CaseCreateUpdateSerializer(serializers.ModelSerializer):
    # Добавляем поле для загрузки изображений при создании/обновлении
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    
    # Поля для создания (только русские)
    title = serializers.CharField(write_only=True, required=False)
    description = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'title_ru', 'title_en', 'description_ru', 'description_en', 'images', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Если пришли поля title и description (создание)
        if 'title' in validated_data:
            title = validated_data.pop('title')
            description = validated_data.pop('description')
            case = Case.objects.create(
                title_ru=title,
                description_ru=description
            )
        else:
            # Если пришли напрямую title_ru, title_en и т.д.
            case = Case.objects.create(**validated_data)
        
        # Создаем изображения для кейса
        for image_data in images_data:
            CaseImage.objects.create(case=case, image=image_data)
        
        return case
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Обновляем поля в зависимости от того, что пришло
        if 'title_ru' in validated_data:
            instance.title_ru = validated_data.get('title_ru', instance.title_ru)
        if 'title_en' in validated_data:
            instance.title_en = validated_data.get('title_en', instance.title_en)
        if 'description_ru' in validated_data:
            instance.description_ru = validated_data.get('description_ru', instance.description_ru)
        if 'description_en' in validated_data:
            instance.description_en = validated_data.get('description_en', instance.description_en)
        
        # Если пришли общие поля (для обратной совместимости)
        if 'title' in validated_data:
            instance.title_ru = validated_data.pop('title')
        if 'description' in validated_data:
            instance.description_ru = validated_data.pop('description')
        
        instance.save()
        
        # Добавляем новые изображения
        for image_data in images_data:
            CaseImage.objects.create(case=instance, image=image_data)
        
        return instance


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video']


class LogoSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    class Meta:
        model = Logo
        fields = ['id', 'title', 'image']
    
    def get_title(self, obj):
        # Определяем язык из запроса
        language = self.context['request'].GET.get('lang', 'ru')
        return obj.title(language)


class TeamSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    
    def get_name(self, obj):
        # Получаем язык из контекста, который передается из API view
        language = self.context.get('language', 'ru')
        return obj.name(language)
    
    def get_description(self, obj):
        language = self.context.get('language', 'ru')
        return obj.description(language)
    
    def get_role(self, obj):
        language = self.context.get('language', 'ru')
        return obj.role(language)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'role', 'photo', 'translation_status']


class TeamAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name_ru', 'name_en', 'description_ru', 'description_en', 
                 'role_ru', 'role_en', 'photo', 'translation_status']

class TeamCreateUpdateSerializer(serializers.ModelSerializer):
    # Поля для создания (только русские) - для обратной совместимости
    name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    description = serializers.CharField(write_only=True, required=False, allow_blank=True)
    role = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'role', 
                 'name_ru', 'name_en', 'description_ru', 'description_en',
                 'role_ru', 'role_en', 'photo', 'translation_status']
        extra_kwargs = {
            'name_ru': {'required': False},
            'name_en': {'required': False},
            'description_ru': {'required': False},
            'description_en': {'required': False},
            'role_ru': {'required': False},
            'role_en': {'required': False},
            'photo': {'required': False},
        }
    
    def create(self, validated_data):
        # Обработка для обратной совместимости
        if 'name' in validated_data and validated_data['name']:
            name_ru = validated_data.pop('name')
            description_ru = validated_data.pop('description', '')
            role_ru = validated_data.pop('role', '')
            
            team_member = Team.objects.create(
                name_ru=name_ru,
                description_ru=description_ru,
                role_ru=role_ru,
                photo=validated_data.get('photo')
            )
        else:
            # Если пришли напрямую name_ru, name_en и т.д.
            team_member = Team.objects.create(**validated_data)
        
        return team_member
    
    def update(self, instance, validated_data):
        # Обработка полей обратной совместимости
        if 'name' in validated_data:
            if validated_data['name']:  # Если не пустой
                instance.name_ru = validated_data.pop('name')
            else:
                validated_data.pop('name')
        
        if 'description' in validated_data:
            if validated_data['description']:
                instance.description_ru = validated_data.pop('description')
            else:
                validated_data.pop('description')
        
        if 'role' in validated_data:
            if validated_data['role']:
                instance.role_ru = validated_data.pop('role')
            else:
                validated_data.pop('role')
        
        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    def to_representation(self, instance):
        # После создания/обновления возвращаем полные данные
        request = self.context.get('request')
        if request and self.is_admin_request(request):
            return TeamAdminSerializer(instance, context=self.context).data
        return TeamSerializer(instance, context=self.context).data
    
    def is_admin_request(self, request):
        """Определяем, является ли запрос админским"""
        if hasattr(request, 'path') and '/admin-panel/' in request.path:
            return True
        if request.query_params.get('admin') == 'true':
            return True
        return False

class NewsSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    # Добавляем явные поля для админки
    title_ru = serializers.CharField(read_only=True)
    title_en = serializers.CharField(read_only=True)
    description_ru = serializers.CharField(read_only=True)
    description_en = serializers.CharField(read_only=True)
    
    def get_title(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'GET'):
            language = request.GET.get('lang', 'ru')
        else:
            language = 'ru'
        return obj.title(language)
    
    def get_description(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'GET'):
            language = request.GET.get('lang', 'ru')
        else:
            language = 'ru'
        return obj.description(language)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'title_ru', 'title_en', 
                 'description_ru', 'description_en', 'image', 'url', 'created_at', 'translation_status']

# Для админки (все поля)
class NewsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title_ru', 'title_en', 'description_ru', 'description_en', 
                 'image', 'url', 'created_at', 'translation_status']


class NewsCreateUpdateSerializer(serializers.ModelSerializer):
    # Поля для обратной совместимости (только для создания)
    title = serializers.CharField(
        write_only=True, 
        required=False, 
        allow_blank=True,
        help_text="Заголовок на русском (для обратной совместимости)"
    )
    description = serializers.CharField(
        write_only=True, 
        required=False, 
        allow_blank=True,
        help_text="Описание на русском (для обратной совместимости)"
    )
    
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'title_ru', 'title_en', 
                 'description_ru', 'description_en', 'image', 'url', 'created_at']
        extra_kwargs = {
            'title_ru': {'required': False},
            'title_en': {'required': False},
            'description_ru': {'required': False},
            'description_en': {'required': False},
            'image': {'required': False},
            'url': {'required': False},
        }
    
    def create(self, validated_data):
        # Для создания: изображение обязательно
        if 'image' not in validated_data or not validated_data['image']:
            raise serializers.ValidationError({
                "image": ["Изображение обязательно для новой новости"]
            })
        
        # Обработка для обратной совместимости
        if 'title' in validated_data and validated_data['title']:
            title_ru = validated_data.pop('title')
            description_ru = validated_data.pop('description', '')
            validated_data['title_ru'] = title_ru
            validated_data['description_ru'] = description_ru
        
        # Проверяем обязательные поля для создания
        if not validated_data.get('title_ru'):
            raise serializers.ValidationError({
                "title_ru": ["Заголовок на русском обязателен"]
            })
        
        return News.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Удаляем поля обратной совместимости, если они пустые
        if 'title' in validated_data:
            if validated_data['title']:  # Если title не пустой
                instance.title_ru = validated_data.pop('title')
            else:
                validated_data.pop('title')
        
        if 'description' in validated_data:
            if validated_data['description']:  # Если description не пустой
                instance.description_ru = validated_data.pop('description')
            else:
                validated_data.pop('description')
        
        # Обновляем только те поля, которые пришли в запросе
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance