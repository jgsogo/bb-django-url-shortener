from django.contrib import admin

from chimp_shortener_data.models import RequestData, UserAgentType


class RequestDataAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'user_agent_type', 'referer', 'link')
    list_filter = ('datetime', 'user_agent_type', 'user_agent_type__is_human',)


class UserAgentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_human')
    list_filter = ('name', 'is_human')


admin.site.register(RequestData, RequestDataAdmin)
admin.site.register(UserAgentType, UserAgentTypeAdmin)