from rest_framework import serializers
from .models import CaseImage, Video, Team, Case
from admin_panel.models import Requests

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'role', 'photo']


class CaseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseImage
        fields = ['id', 'image', 'created_at']

class CaseSerializer(serializers.ModelSerializer):
    images = CaseImageSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'images', 'created_at', 'updated_at']

class CaseCreateUpdateSerializer(serializers.ModelSerializer):
    # Добавляем поле для загрузки изображений при создании/обновлении
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Case
        fields = ['id', 'title', 'description', 'images', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        case = Case.objects.create(**validated_data)
        
        # Создаем изображения для кейса
        for image_data in images_data:
            CaseImage.objects.create(case=case, image=image_data)
        
        return case
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        
        # Обновляем основные поля
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        # Добавляем новые изображения
        for image_data in images_data:
            CaseImage.objects.create(case=instance, image=image_data)
        
        return instance


