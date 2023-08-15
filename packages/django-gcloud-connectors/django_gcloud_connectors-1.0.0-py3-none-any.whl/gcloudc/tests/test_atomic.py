import concurrent.futures
import itertools
import os
import threading
import unittest

import sleuth
from django.db import IntegrityError

from gcloudc.db import transaction
from gcloudc.db.backends.datastore import reset_context_cache
from gcloudc.db.backends.datastore.transaction import TransactionFailedError
from gcloudc.db.decorators import disable_cache
from gcloudc.tests.concurrent_utils import increment_integer_model

from . import TestCase
from .models import (
    IntegerModel,
    Tag,
    TestFruit,
    TestUser,
)


class TransactionTests(TestCase):
    """
    This test case is extended by TransactionTestsExplicitUsingDefault to run the same set of test explicitly
    setting the connection to the default one, and by TransactionTestsNonDefaultConnection to run the same
    set of tests against a different, non-default, connection.

    Always explicitly pass the `using=self.using` when using transaction.atomic, transaction.non_atomic and
    in_atomic_block so that those can be overriden by the child TestCases.
    """

    def test_on_commit_works(self):
        def increment():
            increment.x += 1

        increment.x = 0

        with transaction.atomic(using=self.using):

            transaction.on_commit(increment, using=self.using)
            self.assertEqual(increment.x, 0)

        self.assertEqual(increment.x, 1)

        try:
            with transaction.atomic(using=self.using):
                transaction.on_commit(increment, using=self.using)
                self.assertEqual(increment.x, 1)
                raise ValueError()
        except ValueError:
            pass

        self.assertEqual(increment.x, 1)  # Still the same

        with transaction.atomic(using=self.using):
            pass  # commit hook should have gone with rollback

        self.assertEqual(increment.x, 1)  # Still the same

    def test_get_or_create(self):
        """
            get_or_create uses Django's atomic decorator under the hood
            this can cause issues if called within a gcloudc atomic block
        """

        with transaction.atomic(using=self.using):
            user, created = TestUser.objects.get_or_create(username="foo")
            self.assertTrue(created)

            user, created = TestUser.objects.get_or_create(username="foo")
            self.assertFalse(created)

    def test_repeated_usage_in_a_loop(self):
        pk = TestUser.objects.create(username="foo").pk
        for i in range(4):
            with transaction.atomic(using=self.using):
                TestUser.objects.get(pk=pk)
                continue

        with transaction.atomic(using=self.using):
            TestUser.objects.get(pk=pk)

    def test_recursive_atomic(self):
        lst = []

        @transaction.atomic
        def txn():
            lst.append(True)
            if len(lst) == 3:
                return
            else:
                txn()

        txn()

    def test_recursive_non_atomic(self):
        lst = []

        @transaction.non_atomic(using=self.using)
        def txn():
            lst.append(True)
            if len(lst) == 3:
                return
            else:
                txn()

        txn()

    def test_atomic_in_separate_thread(self):
        """ Regression test.  See #668. """
        @transaction.atomic
        def txn():
            return

        def target():
            txn()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()

    def test_non_atomic_in_separate_thread(self):
        """ Regression test.  See #668. """
        @transaction.non_atomic
        def txn():
            return

        def target():
            txn()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()

    def test_atomic_decorator(self):
        @transaction.atomic(using=self.using)
        def txn():
            TestUser.objects.create(username="foo", field2="bar")
            self.assertTrue(transaction.in_atomic_block(using=self.using))
            raise ValueError()

        with self.assertRaises(ValueError):
            txn()

        self.assertEqual(0, TestUser.objects.count())

    def test_atomic_context_manager(self):
        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="foo", field2="bar")
                raise ValueError()

        self.assertEqual(0, TestUser.objects.count())

    def test_non_atomic_context_manager(self):
        existing = IntegerModel.objects.create(integer_field=1)

        with transaction.atomic(using=self.using):
            self.assertTrue(transaction.in_atomic_block(using=self.using))

            two = IntegerModel.objects.create(integer_field=2)

            with transaction.non_atomic(using=self.using):
                # We're outside the transaction, so two should not exist
                self.assertRaises(
                    IntegerModel.DoesNotExist,
                    IntegerModel.objects.get,
                    pk=two.pk,
                )
                self.assertFalse(transaction.in_atomic_block(using=self.using))
                with sleuth.watch("google.cloud.datastore.client.Client.get") as datastore_get:
                    IntegerModel.objects.get(pk=existing.pk)  # Should hit the cache, not the datastore

                self.assertFalse(datastore_get.called)

            with transaction.atomic(independent=True, using=self.using):
                three = IntegerModel.objects.create(integer_field=3)
                self.assertTrue(transaction.in_atomic_block(using=self.using))

                with transaction.non_atomic(using=self.using):
                    self.assertFalse(transaction.in_atomic_block(using=self.using))
                    self.assertRaises(IntegerModel.DoesNotExist, IntegerModel.objects.get, pk=three.pk)

                    with transaction.non_atomic(using=self.using):
                        self.assertFalse(transaction.in_atomic_block(using=self.using))
                        self.assertRaises(IntegerModel.DoesNotExist, IntegerModel.objects.get, pk=three.pk)

                        with sleuth.watch("google.cloud.datastore.client.Client.get") as datastore_get:
                            # Should hit the cache, not the Datastore
                            IntegerModel.objects.get(pk=existing.pk)
                            self.assertFalse(datastore_get.called)

                    self.assertFalse(transaction.in_atomic_block(using=self.using))
                    self.assertRaises(IntegerModel.DoesNotExist, IntegerModel.objects.get, pk=three.pk)

                # Should hit the cache
                # FIXME: see https://gitlab.com/potato-oss/google-cloud/django-gcloud-connectors/-/issues/44
                # self.assertTrue(IntegerModel.objects.filter(pk=three.pk).exists())
                self.assertTrue(transaction.in_atomic_block(using=self.using))

        self.assertFalse(transaction.in_atomic_block(using=self.using))

    def test_atomic_create_with_unique_constraints(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="one", first_name="one", second_name="one")
                TestUser.objects.create(username="one", first_name="two", second_name="two")

        self.assertEqual(TestUser.objects.count(), 0)

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="one", first_name="a", second_name="b")
                TestUser.objects.create(username="two", first_name="a", second_name="b")

        self.assertEqual(TestUser.objects.count(), 0)

    def test_atomic_bulk_create_with_unique_constraints(self):
        """Test that bulk_create on models with unique constraints preserve those
        within transactions"""
        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.bulk_create([
                    TestUser(username="one", first_name="a", second_name="b"),
                    TestUser(username="one", first_name="a", second_name="b"),
                ])

        self.assertEqual(TestUser.objects.count(), 0)

        TestUser.objects.create(username="one", first_name="one", second_name="one")

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.bulk_create([
                    TestUser(username="two", first_name="a", second_name="b"),
                    TestUser(username="one", first_name="x", second_name="y"),
                ])

        self.assertEqual(TestUser.objects.count(), 1)

    def test_atomic_update_with_unique_constraints(self):
        """Test that unique constraint work as intended when performing an update on
        a model with a unique constraint within an atomic block"""
        one = TestUser.objects.create(username="one", first_name="one", second_name="one")

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="two", first_name="two", second_name="two")
                one.username = "two"
                one.save()

        self.assertEqual(TestUser.objects.count(), 1)

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                two = TestUser.objects.create(username="two", first_name="two", second_name="two")
                two.username = "one"
                one.save()

        self.assertEqual(TestUser.objects.count(), 1)

        two = TestUser.objects.create(username="two", first_name="two", second_name="two")

        with self.assertRaises(IntegrityError):
            with transaction.atomic(using=self.using):
                one.username = "three"
                two.username = "three"
                one.save()
                two.save()

        self.assertEqual(TestUser.objects.count(), 2)

    def test_atomic_bulk_update_with_unique_constraints(self):
        """Test that unique constraint work as intended when performing a bulk update on
        a model with a unique constraint within an atomic block"""
        one = TestUser.objects.create(username="one", first_name="one", second_name="one")
        two = TestUser.objects.create(username="two", first_name="two", second_name="two")
        with self.assertRaises(IntegrityError):
            # This should raise, since the two instances clash with each other
            with transaction.atomic(using=self.using):
                TestUser.objects.all().update(username="three")

        one.refresh_from_db()
        two.refresh_from_db()

        self.assertEqual(one.username, "one")
        self.assertEqual(two.username, "two")

        # This currently doesn't work because Django transforms it in a single UPDATE
        # with a case-when. E.g.
        #
        # ````sql
        # UPDATE table_users
        # SET username = (case when pk = '1' then 'three'
        #                     when pk = '2' then 'four'
        #                 end),
        #
        # WHERE pk in ('1', '2')
        # ```
        # Currently, the connector doesn't know how to deal with that and blows.
        # I think at least in principle we could support this - but not entirely
        # sure we should, as it would end up as a sequence of put anyway - It might
        # need rewriting using `batch` or something like that maybe?
        #
        # with transaction.atomic(using=self.using):
        #     # This should not fail, since the two instances have different values
        #     one.username = "three"
        #     two.username = "four"
        #     TestUser.objects.bulk_update([one, two], ['username'])

    def test_atomic_independent_with_unique_constraints(self):
        """Test that unique constraint work as expected inside atomic blocks"""

        with self.assertRaises(TransactionFailedError):
            with transaction.atomic(using=self.using):
                TestUser.objects.create(username="one", first_name="one", second_name="one")

                with transaction.atomic(independent=True, using=self.using):
                    TestUser.objects.create(username="one", first_name="two", second_name="two")

        # Commented out because it behaves slightly differently depending on concurrency mode
        # With OPTIMISTIC mode, the internal transaction (which is the first to commit) succeeds:
        # all = TestUser.objects.all()
        #
        # self.assertEqual(len(all), 1)
        # self.assertIsNotNone(inner)
        # self.assertEqual(all[0], inner)
        #
        # With PESSIMISTIC mode, the outer transaction acquires a lock, which is never granted to
        # the inner transaction, and the whole operation goes into deadlock and then times out.
        #
        # self.assertEqual(Testuser.objects.count(), 0)

    def test_independent_argument(self):
        """
            We would get a XG error if the inner transaction was not independent
        """
        @transaction.atomic
        def txn1(_username, _fruit):
            @transaction.atomic(independent=True)
            def txn2(_fruit):
                TestFruit.objects.create(name=_fruit, color="pink")
                raise ValueError()

            TestUser.objects.create(username=_username)
            txn2(_fruit)

        with self.assertRaises(ValueError):
            txn1("test", "banana")

    def test_enable_cache_argument(self):
        user = TestUser.objects.create(username="randy", first_name="Randy")

        with sleuth.watch('gcloudc.db.backends.datastore.context.CacheDict.get') as cachedict_get:
            TestUser.objects.get(username="randy")
            self.assertEqual(cachedict_get.call_count, 1)

            with transaction.atomic(enable_cache=False, using=self.using):
                user.first_name = "Łukasz"
                user.save()

                non_cached = TestUser.objects.get(username="randy")
                # Result is not fetched from the cache
                self.assertEqual(non_cached.first_name, "Randy")
                self.assertEqual(cachedict_get.call_count, 1)

    def test_cache_non_unique_model(self):
        with transaction.atomic():
            number = IntegerModel.objects.create(integer_field=123)
            self.assertTrue(IntegerModel.objects.filter(pk=number.pk).exists())

    def test_cache_non_unique_model_refresh(self):
        number = IntegerModel.objects.create(integer_field=123)
        with transaction.atomic():
            self.assertTrue(IntegerModel.objects.filter(pk=number.pk).exists())
            number.integer_field = 321
            number.save()
            number.refresh_from_db()
            self.assertEqual(number.integer_field, 321)

    def test_cache_non_unique_model_delete(self):
        number = IntegerModel.objects.create(integer_field=123)
        with transaction.atomic():
            self.assertTrue(IntegerModel.objects.filter(pk=number.pk).exists())
            number.delete()
            self.assertFalse(IntegerModel.objects.filter(pk=number.pk).exists())

    def test_nested_decorator(self):
        # Nested decorator pattern we discovered can cause a connection_stack
        # underflow.

        @transaction.atomic
        def inner_txn():
            pass

        @transaction.atomic
        def outer_txn():
            inner_txn()

        # Calling inner_txn first puts it in a state which means it doesn't
        # then behave properly in a nested transaction.
        inner_txn()
        outer_txn()

    def test_atomic_context_manager_raises_error(self):
        """Test that the transaction.atomic context manager
        handles errors raised when starting a transaction.
        """
        with sleuth.detonate(
                "gcloudc.db.backends.datastore.transaction.NormalTransaction._enter",
                exception=UserWarning):
            with self.assertRaises(UserWarning):
                with transaction.atomic(using=self.using):
                    TestFruit.objects.create(name="Apple", color="Red")

        self.assertEqual(TestFruit.objects.all().count(), 0)

        # this should not throw a `RuntimeError`;
        # the `transaction.atomic(using=self.using)` context manager should handle errors & cleanup the transaction
        reset_context_cache()

    def test_concurrent_writes(self):
        """
        Test it raises a TransactionFailedError when trying to concurrently update the same object.
        """
        initial_value = 0
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with self.assertRaises(TransactionFailedError):
            with transaction.atomic(using=self.using):
                trx_integer = IntegerModel.objects.get(pk=original_integer.pk)

                with transaction.non_atomic(using=self.using):
                    integer = IntegerModel.objects.get(pk=original_integer.pk)
                    integer.integer_field = integer.integer_field + 10
                    integer.save()

                trx_integer.integer_field = trx_integer.integer_field + 1
                trx_integer.save()

    def test_nested_atomic_create_should_roll_back(self):
        """
        Test that a nested atomic operation is rolled back as part of the rollback
        of the outer atomic block.
        """

        self.assertEqual(IntegerModel.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                IntegerModel.objects.create(integer_field=1)

                with transaction.atomic(using=self.using):
                    Tag.objects.create(name='something')
                raise ValueError()

        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(IntegerModel.objects.count(), 0)

    def test_independent_atomic_create_should_not_roll_back(self):
        """
        Test that an atomic operation with independent=True can succeed even if
        the outer atomic block explodes.
        """

        self.assertEqual(IntegerModel.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                IntegerModel.objects.create(integer_field=1)

                with transaction.atomic(using=self.using, independent=True):
                    Tag.objects.create(name='something')
                raise ValueError()

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(IntegerModel.objects.count(), 0)

    def test_non_atomic_create_should_not_roll_back(self):
        """
        Test that a non_atomic operation can succeed even if outer atomic block explodes.
        """

        self.assertEqual(IntegerModel.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                IntegerModel.objects.create(integer_field=1)

                with transaction.non_atomic(using=self.using):
                    Tag.objects.create(name='something')
                raise ValueError()

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(IntegerModel.objects.count(), 0)

    def test_non_atomic_create_should_not_roll_back_internal_exception(self):
        """
        Test that operations in a non_atomic block before an exception are stored in the db.
        """

        self.assertEqual(IntegerModel.objects.count(), 0)
        self.assertEqual(Tag.objects.count(), 0)

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                IntegerModel.objects.create(integer_field=1)

                with transaction.non_atomic(using=self.using):
                    Tag.objects.create(name='something')
                    raise ValueError()

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(IntegerModel.objects.count(), 0)

    def test_non_atomic_update_should_not_roll_back(self):
        """
        Test that a non_atomic operation can succeed even if
        the outer atomic block explodes.
        """

        integer = IntegerModel.objects.create(integer_field=1)
        tag = Tag.objects.create(name='something')

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                i = IntegerModel.objects.get(pk=integer.pk)
                i.integer_field = 2
                i.save()

                with transaction.non_atomic(using=self.using):
                    tag = Tag.objects.get(pk=tag.pk)
                    tag.name = 'somethingelse'
                    tag.save()
                raise ValueError()

        tag = Tag.objects.get(pk=tag.pk)
        integer = IntegerModel.objects.get(pk=integer.pk)

        self.assertEqual(tag.name, 'somethingelse')
        self.assertEqual(integer.integer_field, 1)

    def test_non_atomic_update_should_not_roll_back_internal_exception(self):
        """
        Test that operations in a non_atomic block before an exception are successful
        """

        integer = IntegerModel.objects.create(integer_field=1)
        tag = Tag.objects.create(name='something')

        with self.assertRaises(ValueError):
            with transaction.atomic(using=self.using):
                i = IntegerModel.objects.get(pk=integer.pk)
                i.integer_field = 2
                i.save()

                with transaction.non_atomic(using=self.using):
                    tag = Tag.objects.get(pk=tag.pk)
                    tag.name = 'somethingelse'
                    tag.save()
                    raise ValueError()

        tag = Tag.objects.get(pk=tag.pk)
        integer = IntegerModel.objects.get(pk=integer.pk)

        self.assertEqual(tag.name, 'somethingelse')
        self.assertEqual(integer.integer_field, 1)

    @unittest.skip("Supposed to fail, leaving as reference")
    def test_unique_constraint_sdk(self):
        """Test that, using the low-level sdk APIs two nested transaction
        fail because of too much contention.

        This test is intended to emulate the equivalent of this in Django land

        ```python
        class TestModel(Model):
            name = CharField(unique=True)

        ...
        with transaction.atomic(using=self.using):
            TestModel.objects.create(name="Jason")

            with transaction.non_atomic(using=self.using):
                TestModel.objects.create(name="Jason")
        ```

        This fails, (and it's ok!) but it may not be obvious why. It's useful to remember
        that because when we have unique constraints, before doing a `put` we perform a `fetch`
        inside a transaction, to ensure there are no constraint violation. This extra
        fetch breaks serialisable isolation, and makes the create (correctly) fail.

        Currently, this test fails in slightly different ways in PESSIMISTIC concurrency
        mode, which is expected. In that mode, the inner transaction can't commit,
        because it cannot acquire the relevant lock.
        This creates a deadlock, which is only broken by a timeout in the APIs.
        """
        from django.db import connection
        from google.cloud import datastore

        local_client = connection.connection.gclient

        with local_client.transaction() as txn:
            query = local_client.query(kind="WithUnique")
            query.add_filter('name', '=', 'Jason')
            res = query.fetch()
            print(list(res))
            key = local_client.key("WithUnique", 1)
            original_entity = datastore.Entity(key=key)
            original_entity["name"] = "Jason"
            txn.put(original_entity)

            with local_client.transaction() as txn2:
                query = local_client.query(kind="WithUnique")
                query.add_filter('name', '=', 'Jason')
                res = query.fetch()
                print(list(res))
                new_key = local_client.key("WithUnique", 2)
                new_entity = datastore.Entity(key=new_key)
                new_entity["name"] = "Jason"
                txn2.put(new_entity)

    @unittest.skip("Supposed to fail, leaving as reference")
    def test_unique_constraint_multiple_connections_sdk(self):
        """Test that, using the low-level sdk APIs two parallell transaction
        fail because of too much contention.

        This test is intended to emulate the equivalend of this in Django land

        ```python
        class TestModel(Model):
            name = CharField(unique=True)

        ...
        # Two requests,  both with name=Jason
        def create_user(request):
            with transaction.atomic(using=self.using):
                TestModel.objects.create(name=request.GET['name'])
        ```
        Because this test doesn't actually run in parallell, but only using
        separate connections in nested transactions for the two requests,
        both `create` actually fail (e.g. the outer transaction fails and is
        rolled back because the inner transaction fails due to contention)

        Currently, this test fails in slightly different ways in PESSIMISTIC concurrency
        mode, which is expected. In that mode, the inner transaction can't commit,
        because it cannot acquire the relevant lock.
        This creates a deadlock, which is only broken by a timeout in the APIs.
        """
        from django.db import connection
        from google.cloud import datastore

        local_client = connection.connection.gclient

        new_connection = connection.copy()
        new_connection.connect()
        local_client2 = new_connection.connection.gclient

        with local_client.transaction() as txn:
            query = local_client.query(kind="WithUnique")
            query.add_filter('name', '=', 'Jason')
            res = query.fetch()
            print(list(res))
            key = local_client.key("WithUnique", 1)
            original_entity = datastore.Entity(key=key)
            original_entity["name"] = "Jason"
            txn.put(original_entity)

            with local_client2.transaction() as txn2:
                query = local_client2.query(kind="WithUnique")
                query.add_filter('name', '=', 'Jason')
                res = query.fetch()
                print(list(res))
                new_key = local_client2.key("WithUnique", 2)
                new_entity = datastore.Entity(key=new_key)
                new_entity["name"] = "Jason"
                txn2.put(new_entity)

    def test_atomic_context_manager_contention_threads(self):
        """
        Test concurrent writes from different threads do not have contention issues.
        """
        initial_value = 0
        concurrent_writes = 10
        futures = []
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_writes) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(increment_integer_model, original_integer.pk, self.using, False))
        concurrent.futures.wait(futures)

        futures_exceptions = [future.exception() for future in futures]
        number_successful_writes = len(list(itertools.filterfalse(None, futures_exceptions)))

        with disable_cache():
            original_integer.refresh_from_db()

        self.assertGreater(number_successful_writes, 0, 'It should save at least an object')
        self.assertEqual(original_integer.integer_field, initial_value + number_successful_writes)

    # TODO(https://gitlab.com/potato-oss/google-cloud/django-gcloud-connectors/-/issues/49)
    # Investigate why this is happining only the CI to make sure we don't have any bugs
    # (ie with the way we manage connections).
    @unittest.skipIf(
        os.environ.get('CI_PROJECT_ID', False),
        'This test on CI does not pass because of a grpc._channel._InactiveRpcError, Socket operation on non-socket'
    )
    def test_atomic_context_manager_contention_processes(self):
        """
        Test concurrent writes from different processes do not have contention issues.
        """
        initial_value = 0
        concurrent_writes = 10
        futures = []
        original_integer = IntegerModel.objects.create(integer_field=initial_value)

        with concurrent.futures.ProcessPoolExecutor(max_workers=concurrent_writes) as executor:
            for _ in range(concurrent_writes):
                futures.append(executor.submit(increment_integer_model, original_integer.pk, self.using, True))
        concurrent.futures.wait(futures)

        futures_exceptions = [future.exception() for future in futures]
        number_successful_writes = len(list(itertools.filterfalse(None, futures_exceptions)))

        with disable_cache():
            original_integer.refresh_from_db()

        self.assertGreater(number_successful_writes, 0, 'It should save at least an object')
        self.assertEqual(original_integer.integer_field, initial_value + number_successful_writes)


class TransactionTestsNonDefaultConnection(TransactionTests):
    """
    This Testcase runs all the tests defined in TransactionTests against a non default connection.
    """
    using = 'non_default_connection'


class TransactionStateTests(TestCase):

    def test_has_already_read(self):
        apple = TestFruit.objects.create(name="Apple", color="Red")
        pear = TestFruit.objects.create(name="Pear", color="Green")

        with transaction.atomic(using=self.using) as txn:
            self.assertFalse(txn.has_already_been_read(apple))
            self.assertFalse(txn.has_already_been_read(pear))

            apple.refresh_from_db()

            self.assertTrue(txn.has_already_been_read(apple))
            self.assertFalse(txn.has_already_been_read(pear))

            with transaction.atomic(using=self.using) as txn:
                self.assertTrue(txn.has_already_been_read(apple))
                self.assertFalse(txn.has_already_been_read(pear))
                pear.refresh_from_db()
                self.assertTrue(txn.has_already_been_read(pear))

                with transaction.atomic(independent=True, using=self.using) as txn2:
                    self.assertFalse(txn2.has_already_been_read(apple))
                    self.assertFalse(txn2.has_already_been_read(pear))

    def test_refresh_if_unread(self):
        apple = TestFruit.objects.create(name="Apple", color="Red")

        with transaction.atomic(using=self.using) as txn:
            apple.color = "Pink"

            txn.refresh_if_unread(apple)

            self.assertEqual(apple.name, "Apple")

            apple.color = "Pink"

            # Already been read this transaction, don't read it again!
            txn.refresh_if_unread(apple)

            self.assertEqual(apple.color, "Pink")


class TransactionInAtomicBlock(TestCase):
    databases = '__all__'

    def test_in_atomic_block_default_in(self):
        with transaction.atomic(using=self.using):
            self.assertTrue(transaction.in_atomic_block())

    def test_in_atomic_block_default_explicit_in(self):
        with transaction.atomic(using='default'):
            self.assertTrue(transaction.in_atomic_block(using='default'))

    def test_in_atomic_block_default_explicit_in_non_default(self):
        with transaction.atomic(using='non_default_connection'):
            self.assertTrue(transaction.in_atomic_block(using='non_default_connection'))

    def test_in_atomic_block_default_out(self):
        self.assertFalse(transaction.in_atomic_block())

    def test_in_atomic_block_default_explicit_out(self):
        self.assertFalse(transaction.in_atomic_block(using='default'))

    def test_in_atomic_block_default_outer_different_connection(self):
        with transaction.atomic(using='non_default_connection'):
            self.assertFalse(transaction.in_atomic_block())

    def test_in_atomic_block_default_explicit_outer_different_connection(self):
        with transaction.atomic(using='non_default_connection'):
            self.assertFalse(transaction.in_atomic_block(using='default'))
