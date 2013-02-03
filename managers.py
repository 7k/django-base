'''Managers for models in the base app.
'''
from django.db.models import Manager
from datetime import datetime


class PublicManager(Manager):
    '''Returns published pages that are not in the future.'''
    def published(self):
        return self.get_query_set().filter(status__gte=2,
                                           publish__lte=datetime.now())
