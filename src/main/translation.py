from modeltranslation.translator import register, TranslationOptions
from .models import Team, Case, Video

@register(Case)
class CaseTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


