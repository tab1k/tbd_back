from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Logo, News, Team, Case, Video

@admin.register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ("id", "name", "role", "photo")
    list_editable = ("name", "role", "photo")

@admin.register(Case)
class CaseAdmin(ModelAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")
    list_editable = ("title", "description")
    readonly_fields = ("created_at", "updated_at")

@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = ("id", "title", "video")
    list_editable = ("title", "video")

@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ("id", "title", "description" , "image", "created_at")
    list_editable = ("title", "description")


@admin.register(Logo)
class LogoAdmin(ModelAdmin):
    list_display = ("id", "title", "image" )
    list_editable = ("title",)


