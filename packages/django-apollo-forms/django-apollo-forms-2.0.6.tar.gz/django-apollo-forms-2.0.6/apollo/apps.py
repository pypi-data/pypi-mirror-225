from __future__ import unicode_literals

from django.apps import AppConfig


class ApolloConfig(AppConfig):
    name = 'apollo'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        super(ApolloConfig, self).ready()
        import apollo.signals
