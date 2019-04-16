from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from .models import Election, Party, Thesis, Answer


class PartyInline(admin.TabularInline):
    model = Party


class ThesisInline(TranslationTabularInline):
    model = Thesis


class AnswerInline(TranslationTabularInline):
    model = Answer


class ElectionAdmin(TranslationAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PartyInline, ThesisInline]

    list_display = (
        'title',
        'accessible_from',
        'accessible_to',
    )


class PartyAdmin(admin.ModelAdmin):
    list_display = (
        'election',
        'short_name',
    )

    list_display_links = ('short_name',)


class ThesisAdmin(TranslationAdmin):
    list_display = (
        'election',
        'topic',
    )

    list_display_links = ('topic',)


class AnswerAdmin(TranslationAdmin):
    list_display = (
        'party',
        'thesis',
        'short_reasoning',
        'stance',
    )

    list_display_links = (
        'short_reasoning',
        'stance',
    )


admin.site.register(Election, ElectionAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Answer, AnswerAdmin)
