from django.contrib import admin
from django import forms
from .models import Video, Team, Case, CaseImage, News, Logo

class AutoTranslateAdmin(admin.ModelAdmin):
    """Базовый класс админки с автопереводом"""
    
    def save_model(self, request, obj, form, change):
        # Автоматический перевод при сохранении через админку
        if change:
            # Проверяем, изменились ли русские поля
            russian_fields_changed = any(
                field.name.endswith('_ru') and field.name in form.changed_data
                for field in obj._meta.fields
            )
            if russian_fields_changed:
                obj.auto_translate()
        else:
            # Для новых объектов
            obj.auto_translate()
        
        super().save_model(request, obj, form, change)
    
    actions = ['auto_translate_selected']
    
    def auto_translate_selected(self, request, queryset):
        """Действие для перевода выбранных записей"""
        for obj in queryset:
            obj.auto_translate()
            obj.save()
        
        self.message_user(request, f"Переведено {queryset.count()} записей")
    auto_translate_selected.short_description = "Автоматически перевести выбранные записи"

@admin.register(Video)
class VideoAdmin(AutoTranslateAdmin):
    list_display = ['title_ru', 'title_en', 'translation_status']
    fieldsets = (
        ('Русская версия', {
            'fields': ('title_ru', 'video')
        }),
        ('Английская версия', {
            'fields': ('title_en', 'translation_status'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Team)
class TeamAdmin(AutoTranslateAdmin):
    list_display = ['name_ru', 'name_en', 'role_ru', 'translation_status']
    fieldsets = (
        ('Русская версия', {
            'fields': ('name_ru', 'description_ru', 'role_ru', 'photo')
        }),
        ('Английская версия', {
            'fields': ('name_en', 'description_en', 'role_en', 'translation_status'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Case)
class CaseAdmin(AutoTranslateAdmin):
    list_display = ['title_ru', 'title_en', 'created_at', 'translation_status']
    fieldsets = (
        ('Русская версия', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('Английская версия', {
            'fields': ('title_en', 'description_en', 'translation_status'),
            'classes': ('collapse',)
        }),
    )

class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 1

@admin.register(News)
class NewsAdmin(AutoTranslateAdmin):
    list_display = ['title_ru', 'title_en', 'created_at', 'translation_status']
    fieldsets = (
        ('Русская версия', {
            'fields': ('title_ru', 'description_ru', 'image', 'url')
        }),
        ('Английская версия', {
            'fields': ('title_en', 'description_en', 'translation_status'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Logo)
class LogoAdmin(AutoTranslateAdmin):
    list_display = ['title_ru', 'title_en', 'translation_status']
    fieldsets = (
        ('Русская версия', {
            'fields': ('title_ru', 'image')
        }),
        ('Английская версия', {
            'fields': ('title_en', 'translation_status'),
            'classes': ('collapse',)
        }),
    )

# CaseImage не требует перевода
admin.site.register(CaseImage)