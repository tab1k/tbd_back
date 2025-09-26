from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Logo, News, Team, Case, Video

admin.site.register(Logo)
admin.site.register(News)
admin.site.register(Team)
admin.site.register(Case)
admin.site.register(Video)


