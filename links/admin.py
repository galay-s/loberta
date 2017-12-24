from django.contrib import admin
from links.models import Link, Interval


class LinkAdmin(admin.ModelAdmin):
    list_display = ['url', 'paused']


class IntervalAdmin(admin.ModelAdmin):
    list_display = ['value']


admin.site.register(Link, LinkAdmin)
admin.site.register(Interval, IntervalAdmin)
