from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import escape
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse

ERROR = 4

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    actions = None
    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'action_flag'
    ]

    search_fields = [
        'user__username',
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'get_action_flag',
        'get_change_message',
    ]

    fieldsets = (
        ('Object Acted Upon', {
            'fields': ('object_id', 'object_repr', 'content_type',)
            }),
        ('Action Details', {
            'fields': ('user', 'action_time', 'action_flag',)
            }),            
        ('Result', {
            'fields': ('change_message',)
            })
        )
    
    def get_change_message(self, obj):
        if not obj.change_message or len(obj.change_message) < 90:
            return obj.change_message
        else:
            return obj.change_message[:90]

    get_change_message.short_description = u'Change Message'        

    def get_action_flag(self, obj):
        action_flag = obj.action_flag
        if action_flag == ADDITION:
            return "Addition"
        elif action_flag == CHANGE:
            return "Change"
        elif action_flag == DELETION:
            return "Deletion"
        elif action_flag == ERROR:
            return "Error"        
        else:
            return action_flag
    get_action_flag.short_description = u'Action Flag'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method != 'POST':
            if request.user.is_superuser or request.user.has_perm("admin.change_logentry"):
                return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        elif not obj.object_id:
            link = "(None)"
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
    
admin.site.register(LogEntry, LogEntryAdmin)
