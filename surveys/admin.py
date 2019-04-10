from django.contrib import admin

from .models import Election, ElectionAdmin
from .models import Party, PartyAdmin
from .models import Thesis, ThesisAdmin
from .models import Answer, AnswerAdmin

admin.site.register(Election, ElectionAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Answer, AnswerAdmin)
