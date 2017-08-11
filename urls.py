'''URLconf for base app.
'''
from django.conf.urls import url

from base.views import PageDetail, Home

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/$',
        view=PageDetail.as_view(),
        name='page'),
    url(r'^$',
        view=Home.as_view(),
        name='home'),
]
