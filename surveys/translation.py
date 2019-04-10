from modeltranslation.translator import register, TranslationOptions
from .models import Election, Thesis, Answer


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
