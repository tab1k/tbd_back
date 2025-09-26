from django.db import models
from django.utils.translation import gettext_lazy as _
from googletrans import Translator
from datetime import datetime

class TranslationMixin:
    """Миксин для автоматического перевода"""
    
    def auto_translate_field(self, text, target_language='en'):
        """Автоматический перевод текста"""
        if not text or not text.strip():
            return ""
        
        try:
            translator = Translator()
            translation = translator.translate(text, dest=target_language)
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return ""

class Video(models.Model):
    title_ru = models.CharField(verbose_name=_("Заголовок (русский)"), max_length=200, blank=True, null=True)
    title_en = models.CharField(verbose_name=_("Заголовок (английский)"), max_length=200, blank=True, null=True)
    video = models.FileField(verbose_name=_("Видео"), upload_to='videos/', blank=False, null=False)
    
    # Статус перевода
    TRANSLATION_STATUS = [
        ('auto', 'Автоматический'),
        ('manual', 'Ручной'),
        ('none', 'Не переведен'),
    ]
    translation_status = models.CharField(
        verbose_name=_("Статус перевода"),
        max_length=10,
        choices=TRANSLATION_STATUS,
        default='none'
    )

    def __str__(self):
        if self.title_ru:
            return self.title_ru
        return f"Video {self.id}"
    
    def title(self, language='ru'):
        """Возвращает заголовок на нужном языке"""
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title_ru or f"Video {self.id}"
    
    def auto_translate(self):
        """Автоматический перевод"""
        if self.title_ru and not self.title_en:
            translated = self.auto_translate_field(self.title_ru, 'en')
            if translated and translated.strip():
                self.title_en = translated
                self.translation_status = 'auto'
    
    def save(self, *args, **kwargs):
        # Автоматический перевод при сохранении
        if self.title_ru and not self.title_en:
            self.auto_translate()
        super().save(*args, **kwargs)
    
    class Meta: 
        verbose_name = _("Видео")
        verbose_name_plural = _("Видео")

class Team(models.Model):
    name_ru = models.CharField(verbose_name=_("Имя (русский)"), max_length=100, blank=True, null=True)
    name_en = models.CharField(verbose_name=_("Имя (английский)"), max_length=100, blank=True, null=True)
    description_ru = models.TextField(verbose_name=_("Описание (русский)"), max_length=350, blank=True, null=True)
    description_en = models.TextField(verbose_name=_("Описание (английский)"), max_length=350, blank=True, null=True)
    role_ru = models.CharField(verbose_name=_("Роль (русский)"), max_length=100, blank=True, null=True)
    role_en = models.CharField(verbose_name=_("Роль (английский)"), max_length=100, blank=True, null=True)
    photo = models.ImageField(verbose_name=_("Фото"), upload_to='team_photos/', blank=True, null=True)
    
    translation_status = models.CharField(
        verbose_name=_("Статус перевода"),
        max_length=10,
        choices=Video.TRANSLATION_STATUS,
        default='none'
    )

    def __str__(self):
        return self.name_ru or f"Team Member {self.id}"
    
    def name(self, language='ru'):
        if language == 'en' and self.name_en:
            return self.name_en
        return self.name_ru or f"Team Member {self.id}"
    
    def description(self, language='ru'):
        if language == 'en' and self.description_en:
            return self.description_en
        return self.description_ru or ""
    
    def role(self, language='ru'):
        if language == 'en' and self.role_en:
            return self.role_en
        return self.role_ru or ""
    
    def auto_translate(self):
        """Автоматический перевод всех полей"""
        translated = False
        
        if self.name_ru and not self.name_en:
            translated_name = self.auto_translate_field(self.name_ru, 'en')
            if translated_name and translated_name.strip():
                self.name_en = translated_name
                translated = True
        
        if self.description_ru and not self.description_en:
            translated_desc = self.auto_translate_field(self.description_ru, 'en')
            if translated_desc and translated_desc.strip():
                self.description_en = translated_desc
                translated = True
            
        if self.role_ru and not self.role_en:
            translated_role = self.auto_translate_field(self.role_ru, 'en')
            if translated_role and translated_role.strip():
                self.role_en = translated_role
                translated = True
            
        if translated:
            self.translation_status = 'auto'
    
    def save(self, *args, **kwargs):
        if any([self.name_ru, self.description_ru, self.role_ru]):
            self.auto_translate()
        super().save(*args, **kwargs)

class Case(models.Model):
    title_ru = models.CharField(verbose_name=_("Заголовок (русский)"), max_length=200, blank=True, null=True)
    title_en = models.CharField(verbose_name=_("Заголовок (английский)"), max_length=200, blank=True, null=True)
    description_ru = models.TextField(verbose_name=_("Описание (русский)"), blank=True, null=True)
    description_en = models.TextField(verbose_name=_("Описание (английский)"), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Создано"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Обновлено"), auto_now=True)
    
    translation_status = models.CharField(
        verbose_name=_("Статус перевода"),
        max_length=10,
        choices=Video.TRANSLATION_STATUS,
        default='none'
    )

    def __str__(self):
        return self.title_ru or f"Case {self.id}"
    
    def title(self, language='ru'):
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title_ru or f"Case {self.id}"
    
    def description(self, language='ru'):
        if language == 'en' and self.description_en:
            return self.description_en
        return self.description_ru or ""

    def auto_translate(self):
        """Автоматический перевод"""
        translated = False
        
        if self.title_ru and not self.title_en:
            translated_title = self.auto_translate_field(self.title_ru, 'en')
            if translated_title and translated_title.strip():
                self.title_en = translated_title
                translated = True
            
        if self.description_ru and not self.description_en:
            translated_desc = self.auto_translate_field(self.description_ru, 'en')
            if translated_desc and translated_desc.strip():
                self.description_en = translated_desc
                translated = True
            
        if translated:
            self.translation_status = 'auto'

    def save(self, *args, **kwargs):
        if any([self.title_ru, self.description_ru]):
            self.auto_translate()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Кейс")
        verbose_name_plural = _("Кейсы")

class CaseImage(models.Model):
    case = models.ForeignKey(Case, verbose_name=_("Кейс"), related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("Изображение"), upload_to='case_images/', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Создано"), auto_now_add=True)

    def __str__(self):
        return f"Image for {self.case.title_ru or 'Case ' + str(self.case.id)}"

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Изображение кейса")
        verbose_name_plural = _("Изображения кейсов")

class News(models.Model):
    title_ru = models.CharField(verbose_name=_("Заголовок (русский)"), max_length=255, blank=True, null=True)
    title_en = models.CharField(verbose_name=_("Заголовок (английский)"), max_length=255, blank=True, null=True)
    description_ru = models.TextField(verbose_name=_("Описание (русский)"), max_length=999, blank=True, null=True)
    description_en = models.TextField(verbose_name=_("Описание (английский)"), max_length=999, blank=True, null=True)
    image = models.ImageField(verbose_name=_("Изображение"), upload_to='news_photos/', blank=False, null=False)
    url = models.URLField(verbose_name=_("Ссылка"), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_("Создано"), auto_now_add=True)
    
    translation_status = models.CharField(
        verbose_name=_("Статус перевода"),
        max_length=10,
        choices=Video.TRANSLATION_STATUS,
        default='none'
    )

    def __str__(self):
        return self.title_ru or f"News {self.id}"
    
    def title(self, language='ru'):
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title_ru or f"News {self.id}"
    
    def description(self, language='ru'):
        if language == 'en' and self.description_en:
            return self.description_en
        return self.description_ru or ""

    def auto_translate(self):
        """Автоматический перевод новости"""
        translated = False
        
        if self.title_ru and not self.title_en:
            translated_title = self.auto_translate_field(self.title_ru, 'en')
            if translated_title and translated_title.strip():
                self.title_en = translated_title
                translated = True
            
        if self.description_ru and not self.description_en:
            translated_desc = self.auto_translate_field(self.description_ru, 'en')
            if translated_desc and translated_desc.strip():
                self.description_en = translated_desc
                translated = True
            
        if translated:
            self.translation_status = 'auto'

    def save(self, *args, **kwargs):
        if any([self.title_ru, self.description_ru]):
            self.auto_translate()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")
        ordering = ['-created_at']

class Logo(models.Model):
    title_ru = models.CharField(verbose_name=_("Название (русский)"), max_length=100, blank=True, null=True)
    title_en = models.CharField(verbose_name=_("Название (английский)"), max_length=100, blank=True, null=True)
    image = models.ImageField(verbose_name=_("Изображение"), upload_to='logo_images/', blank=False, null=False)
    
    translation_status = models.CharField(
        verbose_name=_("Статус перевода"),
        max_length=10,
        choices=Video.TRANSLATION_STATUS,
        default='none'
    )

    def __str__(self):
        return self.title_ru or f"Logo {self.id}"
    
    def title(self, language='ru'):
        if language == 'en' and self.title_en:
            return self.title_en
        return self.title_ru or f"Logo {self.id}"
    
    def auto_translate(self):
        if self.title_ru and not self.title_en:
            translated_title = self.auto_translate_field(self.title_ru, 'en')
            if translated_title and translated_title.strip():
                self.title_en = translated_title
                self.translation_status = 'auto'

    def save(self, *args, **kwargs):
        if self.title_ru:
            self.auto_translate()
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = _("Логотип")
        verbose_name_plural = _("Логотипы")

# Добавляем миксин ко всем моделям
for model_name in ['Video', 'Team', 'Case', 'News', 'Logo']:
    model_class = globals()[model_name]
    model_class.auto_translate_field = TranslationMixin.auto_translate_field