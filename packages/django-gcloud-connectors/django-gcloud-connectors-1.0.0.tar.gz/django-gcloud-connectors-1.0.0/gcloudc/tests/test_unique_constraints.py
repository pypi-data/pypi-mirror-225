import concurrent.futures
from unittest import skip

import sleuth
from django.db import connection
from django.db.models import Model
from django.db.utils import IntegrityError
from gcloudc.db import transaction

from gcloudc.db.backends.datastore.transaction import TransactionFailedError
from gcloudc.db.models.fields.charfields import CharField

from . import TestCase
from .models import (
    NullableUniqueTogether,
    TestUser,
    TestUserTwo,
)


def _get_client():
    return connection.connection.gclient


def get_kind_query(kind, keys_only=True):
    datastore_client = _get_client()
    query = datastore_client.query(kind=kind)
    if keys_only:
        query.keys_only()
    return list(query.fetch())


class TestUniqueConstraints(TestCase):

    KINDS_TO_DELETE = [
        "uniquemarker", "test_testuser", "test_testusertwo", "test_nullableuniquetogether"
    ]

    def test_insert(self):
        """
        Assert that when creating a new instance, unique markers are also
        created to reflect the constraints defined on the model.

        If a subsequent insert is attempted, these should be compared to
        enforce a constraint similar to SQL.
        """
        TestUser.objects.create(username="tommyd", first_name="Tommy", second_name="Shelby")

        # attempt to create another entity which violates one of the constraints
        with self.assertRaises(IntegrityError):
            TestUser.objects.create(username="tommyd", first_name="Tommy", second_name="Doherty")

    def test_insert_unique_together(self):
        """
        Assert that when creating a new instance, unique markers are also
        created to reflect the constraints defined on the model.

        If a subsequent insert is attempted, these should be compared to
        enforce a constraint similar to SQL.
        """
        TestUser.objects.create(username="tommyd", first_name="Tommy", second_name="Doherty")

        # attempt to create another entity which violates a unique_together constraint
        with self.assertRaises(IntegrityError):
            TestUser.objects.create(username="thetommyd", first_name="Tommy", second_name="Doherty")

    def test_bulk_insert(self):
        """
        Assert that bulk inserts respect any unique markers made inside
        the same transaction.
        """
        with self.assertRaises(IntegrityError):
            TestUserTwo.objects.bulk_create(
                [
                    TestUserTwo(username="Mickey Bell"),
                    TestUserTwo(username="Tony Thorpe"),
                    TestUserTwo(username="Mickey Bell"),
                ]
            )

        self.assertEqual(TestUserTwo.objects.count(), 0)

        # sanity check normal bulk insert works
        TestUserTwo.objects.bulk_create([TestUserTwo(username="Mickey Bell"), TestUserTwo(username="Tony Thorpe")])
        self.assertEqual(TestUserTwo.objects.count(), 2)

        # and if we were to run the bulk insert, previously created
        # unique markers are still respected
        with self.assertRaises(IntegrityError):
            TestUserTwo.objects.bulk_create([TestUserTwo(username="Mickey Bell"), TestUserTwo(username="Tony Thorpe")])
        self.assertEqual(TestUserTwo.objects.count(), 2)

    def test_update_with_constraint_conflict(self):
        TestUserTwo.objects.create(username="AshtonGateEight")
        user_two = TestUserTwo.objects.create(username="AshtonGateSeven")

        # now do the update operation
        user_two.username = "AshtonGateEight"
        with self.assertRaises(IntegrityError):
            user_two.save()

    def test_update_with_constraint_together_conflict(self):
        TestUser.objects.create(username="tommyd", first_name="Tommy", second_name="Doherty")
        user_two = TestUser.objects.create(username="tommye", first_name="Tommy", second_name="Einfield")

        # now do the update operation
        user_two.second_name = "Doherty"
        with self.assertRaises(IntegrityError):
            user_two.save()

    def test_error_on_update_does_not_change_entity(self):
        """
        Assert that when there is an error / exception raised as part of the
        update command, the entity is rolled back to its originial state.
        """
        user = TestUserTwo.objects.create(username="AshtonGateEight")

        with sleuth.detonate("gcloudc.db.backends.datastore.transaction.Transaction.put", TransactionFailedError):
            with self.assertRaises(TransactionFailedError):
                user.username = "Red Army"
                user.save()

        user.refresh_from_db()
        self.assertEqual(user.username, "AshtonGateEight")

    def test_bulk_update(self):
        """
        Assert that updates via the QuerySet API handle uniques.
        """
        user_one = TestUser.objects.create(username="stevep", first_name="steve", second_name="phillips")
        user_two = TestUser.objects.create(username="joeb", first_name="joe", second_name="burnell")

        # now do the update operation on the queryset
        TestUser.objects.all().update(first_name="lee")

        user_one.refresh_from_db()
        user_two.refresh_from_db()

        self.assertEqual(user_one.first_name, "lee")
        self.assertEqual(user_two.first_name, "lee")

    def test_error_with_bulk_update(self):
        user_one = TestUser.objects.create(username="stevep", first_name="steve", second_name="phillips")
        user_two = TestUser.objects.create(username="joeb", first_name="joe", second_name="burnell")

        with self.assertRaises(IntegrityError):
            TestUser.objects.all().update(username="stevep")

        user_one.refresh_from_db()
        user_two.refresh_from_db()

        # in Djangae (python 2) this doesn't work, user_two would end up
        # with username=bill, which makes it non transactional on the group
        self.assertEqual(user_one.username, "stevep")
        self.assertEqual(user_two.username, "joeb")

    def test_error_with_bulk_update_in_memory(self):
        user_one = TestUser.objects.create(username="stevep", first_name="steve", second_name="phillips")
        user_two = TestUser.objects.create(username="joeb", first_name="joe", second_name="burnell")

        with self.assertRaises(IntegrityError):
            TestUser.objects.all().update(username="bill")

        user_one.refresh_from_db()
        user_two.refresh_from_db()

        self.assertEqual(user_one.username, "stevep")
        self.assertEqual(user_two.username, "joeb")

    def test_error_with_bulk_update_unique_together(self):
        user_one = TestUser.objects.create(username="stevep", first_name="steve", second_name="phillips")
        user_two = TestUser.objects.create(username="joeb", first_name="joe", second_name="burnell")

        with self.assertRaises(IntegrityError):
            TestUser.objects.all().update(first_name="lee", second_name="bruce")

        user_one.refresh_from_db()
        user_two.refresh_from_db()

        # in djangae (python 2) this doesn't work, user_two would end up
        # with username=bill, which makes it non transactional on the group
        self.assertEqual(user_one.first_name, "steve")
        self.assertEqual(user_two.first_name, "joe")

    def test_error_with_bulk_update_unique_together_in_memory(self):
        user_one = TestUser.objects.create(username="stevem", first_name="steve", second_name="mitchell")
        user_two = TestUser.objects.create(username="joem", first_name="joe", second_name="mitchell")

        with self.assertRaises(IntegrityError):
            TestUser.objects.all().update(first_name="lee")

        user_one.refresh_from_db()
        user_two.refresh_from_db()

        self.assertEqual(user_one.first_name, "steve")
        self.assertEqual(user_two.first_name, "joe")

    def test_multithread_unique(self):
        """
        Ensure that with multiple insert in parallell, only one is accepted
        """
        # Keeping this number large, to increase the chance it will actually fail if there is
        # contention (otherwise it'd be the same as the "serial" example)
        concurrent_writes = 10

        def create_user():
            TestUserTwo.objects.create(username="contentious")

        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_writes) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(create_user))

        concurrent.futures.wait(futures)

        futures_exceptions = [
            future.exception()
            for future in futures
            if future.exception() is not None
        ]

        self.assertEqual(len(futures_exceptions), concurrent_writes - 1)
        self.assertEqual(TestUserTwo.objects.count(), 1)

    # see https://github.com/googleapis/google-cloud-python/issues/9921
    @skip("This test should (probably) not fail once the emulator bug is fixed")
    def test_500_limit(self):
        # TODO: datastore emulator seems to fail at the old 25 limit, update
        # this test once emulator issue is addressed
        for i in range(25):
            username = "stevep_{}".format(i)
            first_name = "steve_{}".format(i)
            second_name = "phillips_{}".format(i)
            TestUser.objects.create(
                username=username,
                first_name=first_name,
                second_name=second_name,
            )

        TestUser.objects.all().update(first_name="lee")

        for i in range(25, 501):
            username = "stevep_{}".format(i)
            first_name = "steve_{}".format(i)
            second_name = "phillips_{}".format(i)
            TestUser.objects.create(
                username=username,
                first_name=first_name,
                second_name=second_name,
            )

        # This should raise because of the 500 changes per transaction limit
        with self.assertRaises(IntegrityError):
            TestUser.objects.all().update(first_name="lee")

    def test_bulk_delete_fails_if_limit_exceeded(self):
        """
        Assert that there is currently a practical limitation when deleting multi
        entities, based on a combination of the unique markers per model
        and transaction limit of touching 500 entities.
        """
        TestUserTwo.objects.create(username="Mickey Bell")
        TestUserTwo.objects.create(username="Tony Thorpe")

        with sleuth.switch("gcloudc.db.backends.datastore.transaction.TRANSACTION_ENTITY_LIMIT", 1):
            with self.assertRaises(Exception):
                TestUserTwo.objects.all().delete()

    def test_delete_entity_fails(self):
        """
        Assert that if the entity delete operation fails, the user is not deleted.
        """
        user = TestUserTwo.objects.create(username="Mickey Bell")

        with sleuth.detonate(
            "gcloudc.db.backends.datastore.commands.remove_entities_from_cache_by_key", TransactionFailedError
        ):
            with self.assertRaises(TransactionFailedError):
                user.delete()

        # the entity in question should not have been deleted, as error in the
        # transactions atomic block should revert all changes
        user.refresh_from_db()

    def test_polymodels_with_base_unique(self):
        """
        Test that a polymodel unique constraint doesn't blow when the parent
        class has a unique constraint
        """
        class Base(Model):
            unique_field = CharField(unique=True)

        class Child(Base):
            pass

        # This used to raise an integrity error because the field was checked
        # for both base and Child class
        child = Child.objects.create(unique_field="unique_value")
        self.assertIsNotNone(child)

        # Check that actual integrity issues are reported
        with self.assertRaises(IntegrityError):
            Child.objects.create(unique_field="unique_value")

    def test_polymodels_with_child_unique(self):
        """
        Test that a polymodel unique constraint doesn't blow when the child
        class has a unique constraint
        """
        class Base(Model):
            pass

        class Child(Base):
            unique_field = CharField(unique=True)

        child = Child.objects.create(unique_field="unique_value")
        self.assertIsNotNone(child)

        with self.assertRaises(IntegrityError):
            Child.objects.create(unique_field="unique_value")

    def test_polymodels_with_base_unique_together(self):
        """
        Test that a polymodel unique_together constraint is respected when
        in the parent model
        """
        class Base(Model):
            a = CharField()
            b = CharField()

            class Meta():
                unique_together = ["a", "b"]

        class Child(Base):
            pass

        child = Child.objects.create(a="a", b="b")
        self.assertIsNotNone(child)

        # Check that actual integrity issues are reported
        with self.assertRaises(IntegrityError):
            child = Child.objects.create(a="a", b="b")

    def test_polymodels_with_child_unique_together(self):
        """
        Test that a polymodel unique_together constraint is respected when
        in the child model
        """
        class Base(Model):
            pass

        class Child(Base):
            a = CharField()
            b = CharField()

            class Meta():
                unique_together = ["a", "b"]

        child = Child.objects.create(a="a", b="b")
        self.assertIsNotNone(child)

        # Check that actual integrity issues are reported
        with self.assertRaises(IntegrityError):
            child = Child.objects.create(a="a", b="b")

    def test_polymodels_with_cross_model_unique_together(self):
        """
        Test that a polymodel unique_together constraint is respected when
        it references fields across the hierarchy

        Note: this wouldn't work with a SQL backend because unique constraint
        are per-table. Since we are doing read-before-write to enforce  unique
        constraint, table structures is not a problem.
        """
        class Base(Model):
            a = CharField()

        class Child(Base):
            b = CharField()

            class Meta():
                unique_together = ["a", "b"]

        child = Child.objects.create(a="a", b="b")
        self.assertIsNotNone(child)

        # Check that actual integrity issues are reported
        with self.assertRaises(IntegrityError):
            child = Child.objects.create(a="a", b="b")

    def test_unique_in_abstract_parent(self):
        """
        Test that a polymodel unique constraint doesn't blow when the parent
        class has a unique constraint
        """
        class Base(Model):
            unique_field = CharField(unique=True)

            class Meta():
                abstract = True

        class Child(Base):
            pass

        child = Child.objects.create(unique_field="unique_value")
        self.assertIsNotNone(child)

        # Check that actual integrity issues are reported
        with self.assertRaises(IntegrityError):
            Child.objects.create(unique_field="unique_value")

    def test_unique_together_with_null(self):
        """ If one of the field values in a unique_together constraint is null then the whole
            combination should be ignored for that object.
        """
        # This is the expected behaviour based on Postgres:
        # https://www.postgresql.org/docs/13/ddl-constraints.html#DDL-CONSTRAINTS-UNIQUE-CONSTRAINTS
        NullableUniqueTogether.objects.create(field1=1, field2=2, field3=None)
        NullableUniqueTogether.objects.create(field1=1, field2=2, field3=None)

    def test_create_and_re_save(self):
        """
        Test creating an object, updating a non unique field and re-saving it
        does not raise a unique constraing error.
        """
        user = TestUser.objects.create(username="tommyd", first_name="Tommy", second_name="Shelby")
        user.field2 = 'updated'
        user.save()

    def test_create_and_save_in_transaction(self):
        """
        Test creating an object, updating a non-unique field and re-saving it within a transaction
        does not raise a unique constraing error.
        """
        with transaction.atomic():
            user = TestUser.objects.create(username="tommyd", first_name="Tommy", second_name="Shelby")
            user.field2 = 'updated'
            user.save()
