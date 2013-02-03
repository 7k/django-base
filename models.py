import datetime

from django.contrib.auth.models import User
from django.db import models

from managers import PublicManager


class Page(models.Model):
    '''Page model.
    '''
    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
    )
    title = models.CharField('title', max_length=200)
    slug = models.SlugField('slug', unique=True)
    author = models.ForeignKey(User, blank=True, null=True,
                               related_name='pages')
    body = models.TextField('body', blank=True)
    status = models.IntegerField('status', choices=STATUS_CHOICES, default=2)
    publish = models.DateTimeField('publish', default=datetime.datetime.now)
    show_publish = models.BooleanField('show publish', default=True,
                                       help_text='Whether or not to show '
                                       'the published date on the page')
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)
    objects = PublicManager()

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        db_table = 'base_pages'
        ordering = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('page', None, {'slug': self.slug})