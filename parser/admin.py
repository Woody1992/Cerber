from django.contrib import admin
from parser.models import InstagramAccount, ParserRun


class InstagramAccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'status', 'created_at']
    search_fields = ['username']
    list_filter = ['status']
    list_editable = ['status']
    list_per_page = 10


class ParserRunAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'status', 'worker_id']
    list_filter = ['status']
    list_per_page = 100


admin.site.register(InstagramAccount, InstagramAccountAdmin)
admin.site.register(ParserRun, ParserRunAdmin)
