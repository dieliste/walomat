from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings, Election, Thesis, Answer


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('welcome_text', )


@register(Election)
class ElectionTranslationOptions(TranslationOptions):
    fields = ('title', )


@register(Thesis)
class ThesisTranslationOptions(TranslationOptions):
    fields = (
        'topic',
        'thesis',
    )


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ('reasoning', )
