from django.contrib import admin

from shortener.models import Link

class LinkAdmin(admin.ModelAdmin):
    list_display = ('_hash','url', 'created')
    list_filter = ('created',)

admin.site.register(Link, LinkAdmin)
