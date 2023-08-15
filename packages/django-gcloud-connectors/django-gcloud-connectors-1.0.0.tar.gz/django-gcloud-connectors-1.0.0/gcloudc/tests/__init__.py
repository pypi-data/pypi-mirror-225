from django.test import TestCase as DjangoTestCase
from django.db import connection

from gcloudc.tests.router import Router


class TestCase(DjangoTestCase):
    databases = '__all__'
    using = 'default'

    def setUp(self):
        connection.connect()  # Make sure we have a connection
        Router.activate_connection(self.using)
        super().setUp()

    # This was mistakenly renamed to assertCountsEqual
    # in Python 3, so this avoids any complications arising
    # when they rectify that! https://bugs.python.org/issue27060
    def assertItemsEqual(self, lhs, rhs):
        if set(lhs) != set(rhs):
            raise AssertionError("Items were not the same in both lists")
