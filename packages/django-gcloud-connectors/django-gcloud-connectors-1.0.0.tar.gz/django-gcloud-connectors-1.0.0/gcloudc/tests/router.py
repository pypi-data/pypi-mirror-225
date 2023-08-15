from django.conf import settings
from typing import Optional


class Router:
    """Route DB queries depending on selected connection."""

    connection_conf = settings.DATABASES
    active_connection = 'default'

    @classmethod
    def activate_connection(cls, connection_alias: Optional[str] = None):
        """All read and writes will be executed against the given connection"""
        if connection_alias is None:
            connection_alias = 'default'

        assert connection_alias in cls.connection_conf, f"Router: given connection {connection_alias} not configured."
        cls.active_connection = connection_alias

    def db_for_read(self, model, **hints):
        return Router.active_connection

    def db_for_write(self, model, **hints):
        return Router.active_connection
