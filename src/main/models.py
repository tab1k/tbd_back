from email.mime import image
from pyexpat import model
from tabnanny import verbose
from turtle import mode
from django.db import models
from django.utils.translation import gettext_lazy as _


class Video(models.Model):
    title = models.CharField(verbose_name=_("Заголовок"),max_length=200, blank=True, null=True)
    video = models.FileField(verbose_name=_("Видео"),upload_to='videos/', blank=False, null=False)

    def __str__(self):
        if self.title:
            return self.title
        return f"Video {self.id}"
    
    class Meta: 
        verbose_name = _("Видео")

class Team(models.Model):
    name = models.CharField(verbose_name=_("Название"),max_length=100, blank=True, null=True)
    role = models.CharField(verbose_name=_("Роль"),max_length=100, blank=True, null=True)
    photo = models.ImageField(verbose_name=_("Фото"),upload_to='team_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Case(models.Model):
    title = models.CharField(verbose_name=_("Заголовок"),max_length=200, blank=True, null=True)
    description = models.TextField(verbose_name=_("Описание"),blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Обновлено"),auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(verbose_name=_("Создано"),auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title or f"Case {self.id}"

    class Meta:
        ordering = ['-created_at']

class CaseImage(models.Model):
    case = models.ForeignKey(Case, verbose_name=_("Кейс"), related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("Изображение"), upload_to='case_images/', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Создано"),auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.case.title or 'Case ' + str(self.case.id)}"

    class Meta:
        ordering = ['created_at']


class News(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(max_length=999, blank=True, null=True)
    image = models.ImageField(upload_to='news_photos/', blank=False, null=False)
    
    url = models.URLField(blank=True, null=True, verbose_name='Ссылка')

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Logo(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='logo_images/', blank=False, null=False)

        
    class Meta:
        verbose_name = 'Логотип'
        verbose_name_plural = 'Логотипы'
