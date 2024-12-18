from django.contrib import admin
from .models import Manager, Event, Perdorues, PerdoruesJoinsEvent
# Register your models here.

admin.site.register(Manager)
admin.site.register(Event)
admin.site.register(Perdorues)
admin.site.register(PerdoruesJoinsEvent)
