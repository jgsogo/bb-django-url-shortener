from django.contrib import admin

from shortener_data.models import RequestData, UserAgent, UserAgentType


class RequestDataAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'user_agent', 'referer', 'link')
    list_filter = ('datetime', 'user_agent', 'user_agent__typ',)


class UserAgentAdmin(admin.ModelAdmin):
    list_display = ('typ', 'name', 'company', '_hit_robots')
    list_filter = ('typ',)


class UserAgentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(RequestData, RequestDataAdmin)
admin.site.register(UserAgent, UserAgentAdmin)
admin.site.register(UserAgentType, UserAgentTypeAdmin)