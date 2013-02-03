'''Admin classes for base app.
'''
from django.contrib import admin

from base.models import Page


class PageAdmin(admin.ModelAdmin):
    '''Admin class for `GenericPage` model.'''
    list_display = ('title', 'publish', 'status')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Page, PageAdmin)
