from django.contrib import admin
from django.utils.html import format_html

from .models import Ticket, TicketNote, Project


class TicketNoteInline(admin.StackedInline):
    model = TicketNote
    fields = ('note_id', 'content', 'updated_at')
    readonly_fields = ('content', 'updated_at')
    extra = 0


class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'summary', 'updated_at')
    search_fields = ('ticket_id', 'summary', 'ticketnote__content')
    inlines = [
        TicketNoteInline,
    ]


class TicketNoteAdmin(admin.ModelAdmin):
    list_display = ('note_id', 'ticket_id', 'updated_at')
    search_fields = ('ticket_id', 'content')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'name')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketNote, TicketNoteAdmin)
