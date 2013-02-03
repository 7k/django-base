'''Base app views.
'''
from django.views.generic import DetailView

from base.models import Page


class PageDetail(DetailView):
    '''Displays a generic page. If user is superuser, view will display
    unpublished page detail for previewing purposes.
    '''
    model = Page

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Page.objects.all()
        else:
            return Page.objects.published()

class Home(PageDetail):
    '''Displays the home page.
    '''
    template_name='base/home.html'

    def get_object(self):
        page, _created = Page.objects.get_or_create(slug='home')
        return page