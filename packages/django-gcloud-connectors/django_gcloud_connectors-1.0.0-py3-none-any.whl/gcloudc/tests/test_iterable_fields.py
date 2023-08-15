import datetime

from django import forms
from django.core import serializers
from django.core.exceptions import (
    ImproperlyConfigured,
    ValidationError,
)
from django.db import (
    NotSupportedError,
    models,
)

from gcloudc.db.models.fields.charfields import CharField
from gcloudc.db.models.fields.iterable import (
    ListField,
    SetField,
)
from gcloudc.db.models.fields.related import (
    RelatedListField,
    RelatedSetField,
)

from . import TestCase


class IterableIterableRelatedModel(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return "%s:%s" % (self.pk, self.name)

    class Meta:
        app_label = "gcloudc"


class IterableIterableFieldsWithValidatorsModel(models.Model):
    set_field = SetField(models.CharField(max_length=100), min_length=2, max_length=3, blank=False)

    list_field = ListField(models.CharField(max_length=100), min_length=2, max_length=3, blank=False)

    related_set = RelatedSetField(IterableIterableRelatedModel, min_length=2, max_length=3, blank=False)

    related_list = RelatedListField(
        IterableIterableRelatedModel, related_name="iterable_list", min_length=2, max_length=3, blank=False
    )


class IterableFieldModel(models.Model):
    set_field = SetField(models.CharField(max_length=1))
    list_field = ListField(models.CharField(max_length=1))
    set_field_int = SetField(models.BigIntegerField(max_length=1))
    list_field_int = ListField(models.BigIntegerField(max_length=1))
    set_field_dt = SetField(models.DateTimeField())
    list_field_dt = ListField(models.DateTimeField())

    class Meta:
        app_label = "gcloudc"


class IterableFieldTests(TestCase):
    def test_filtering_on_iterable_fields(self):
        list1 = IterableFieldModel.objects.create(
            list_field=["A", "B", "C", "D", "E", "F", "G"], set_field=set(["A", "B", "C", "D", "E", "F", "G"])
        )
        list2 = IterableFieldModel.objects.create(
            list_field=["A", "B", "C", "H", "I", "J"], set_field=set(["A", "B", "C", "H", "I", "J"])
        )

        for field in ("list_field", "set_field"):
            # Filtering using __contains lookup with single value. This is just a
            # convenience/backwards compatibility thing.
            qry = IterableFieldModel.objects.filter(**{f"{field}__contains": "A"})
            self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk, list2.pk]))
            # filtering using __contains lookup
            qry = IterableFieldModel.objects.filter(**{f"{field}__contains": ["A"]})
            self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk, list2.pk]))
            qry = IterableFieldModel.objects.filter(**{f"{field}__contains": ["H"]})
            self.assertEqual(sorted(x.pk for x in qry), [list2.pk])
            # Filtering using two __contains filters, applied together
            qry = IterableFieldModel.objects.filter(**{f"{field}__contains": ["A", "D"]})
            self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk]))
            # Filtering using two __contains filters, applied one after the other
            qry = IterableFieldModel.objects.filter(
                **{f"{field}__contains": ["A"]}
            ).filter(
                **{f"{field}__contains": ["B"]}
            )
            self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk, list2.pk]))
            qry = IterableFieldModel.objects.filter(
                **{f"{field}__contains": ["A"]}
            ).filter(
                **{f"{field}__contains": ["J"]}
            )
            self.assertEqual(list(qry), [list2])
            # Filtering using *three* __contains filters. See GitLab ticket #28.
            qry = IterableFieldModel.objects.filter(
                **{f"{field}__contains": ["A"]}
            ).filter(
                **{f"{field}__contains": ["B"]}
            ).filter(
                **{f"{field}__contains": ["C"]}
            )
            self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk, list2.pk]))
            qry = IterableFieldModel.objects.filter(
                **{f"{field}__contains": ["A"]}
            ).filter(
                **{f"{field}__contains": ["G"]}
            ).filter(
                **{f"{field}__contains": ["J"]}
            )
            self.assertEqual(len(qry), 0)
            # Filtering using PK plus __contains filter
            qry = IterableFieldModel.objects.filter(**{
                "pk": list1.pk,
                f"{field}__contains": ["A"]
            })
            self.assertEqual(list(qry), [list1])
            qry = IterableFieldModel.objects.filter(**{
                "pk": list1.pk,
                f"{field}__contains": ["A"]
            }).filter(
                **{f"{field}__contains": ["B"]}
            )
            self.assertEqual(list(qry), [list1])
            qry = IterableFieldModel.objects.filter(**{
                "pk": list1.pk,
                f"{field}__contains": ["J"]
            })
            self.assertEqual(len(qry), 0)

        # filtering using __overlap lookup with ListField:
        qry = IterableFieldModel.objects.filter(list_field__overlap=["A", "B", "C"])
        self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk, list2.pk]))
        qry = IterableFieldModel.objects.filter(list_field__overlap=["H", "I", "J"])
        self.assertEqual(sorted(x.pk for x in qry), sorted([list2.pk]))

        # filtering using __overlap lookup with SetField:
        qry = IterableFieldModel.objects.filter(set_field__overlap=set(["A", "B"]))
        self.assertEqual(sorted(x.pk for x in qry), sorted([list1.pk, list2.pk]))
        qry = IterableFieldModel.objects.filter(set_field__overlap=["H"])
        self.assertEqual(sorted(x.pk for x in qry), [list2.pk])

        # Filtering using two __overlap filters, applied one after the other
        qry = IterableFieldModel.objects.filter(
                **{"list_field__overlap": ["A"]}
            ).filter(
                **{"list_field__overlap": ["J"]}
            )
        self.assertEqual(list(qry), [list2])

        # Filtering with combination of __contains and __overlap filters, in either order.
        qry = IterableFieldModel.objects.filter(
                **{"list_field__contains": ["A", "D"]}
            ).filter(
                **{"list_field__overlap": ["B", "J"]}
            )
        self.assertEqual(list(qry), [list1])
        qry = IterableFieldModel.objects.filter(
                **{"list_field__overlap": ["B", "J"]}
            ).filter(
                **{"list_field__contains": ["A", "D"]}
            )
        self.assertEqual(list(qry), [list1])

        # Combine multiple __contains with pk__in
        qry = IterableFieldModel.objects.filter(
                **{"list_field__contains": ["A"]}
            ).filter(
                **{"list_field__contains": ["G"]}
            ).filter(
                **{"pk__in": [list1.pk, list2.pk]}
            )
        self.assertEqual(list(qry), [list1])
        qry = IterableFieldModel.objects.filter(
                **{"list_field__contains": ["A"]}
            ).filter(
                **{"list_field__contains": ["B"]}
            ).filter(
                **{"pk__in": [list1.pk]}
            )
        self.assertEqual(list(qry), [list1])

    def test_empty_iterable_fields(self):
        """ Test that an empty set field always returns set(), not None """
        instance = IterableFieldModel()
        # When assigning
        self.assertEqual(instance.set_field, set())
        self.assertEqual(instance.list_field, [])
        instance.save()

        instance = IterableFieldModel.objects.get()
        # When getting it from the db
        self.assertEqual(instance.set_field, set())
        self.assertEqual(instance.list_field, [])

    def test_filtering_multiple_contains_and_pk_in(self):
        A = IterableFieldModel.objects.create(list_field=["A"])
        IterableFieldModel.objects.create(list_field=["B"])
        AB = IterableFieldModel.objects.create(list_field=["A", "B"])
        IterableFieldModel.objects.create(list_field=["A", "B", "C"])

        qry = (
            IterableFieldModel.objects
            .filter(list_field__contains='A')
            .filter(list_field__contains='B')
            .filter(pk__in=[A.pk, AB.pk])
        )
        self.assertEqual(set(qry), {AB})

    def test_list_field(self):
        instance = IterableFieldModel.objects.create()
        self.assertEqual([], instance.list_field)
        instance.list_field.append("One")
        self.assertEqual(["One"], instance.list_field)
        instance.save()

        self.assertEqual(["One"], instance.list_field)

        instance = IterableFieldModel.objects.get(pk=instance.pk)
        self.assertEqual(["One"], instance.list_field)

        results = IterableFieldModel.objects.filter(list_field__contains=["One"])
        self.assertEqual([instance], list(results))

        self.assertEqual([1, 2], ListField(models.IntegerField).to_python("[1, 2]"))

    def test_set_field(self):
        instance = IterableFieldModel.objects.create()
        self.assertEqual(set(), instance.set_field)
        instance.set_field.add("One")
        self.assertEqual(set(["One"]), instance.set_field)
        instance.save()

        self.assertEqual(set(["One"]), instance.set_field)

        instance = IterableFieldModel.objects.get(pk=instance.pk)
        self.assertEqual(set(["One"]), instance.set_field)

        self.assertEqual({1, 2}, SetField(models.IntegerField).to_python("[1, 2]"))

    def test_empty_list_queryable_with_is_null(self):
        instance = IterableFieldModel.objects.create()

        self.assertTrue(IterableFieldModel.objects.filter(set_field__isempty=True).exists())

        instance.set_field.add(1)
        instance.save()

        self.assertFalse(IterableFieldModel.objects.filter(set_field__isempty=True).exists())
        self.assertTrue(IterableFieldModel.objects.filter(set_field__isempty=False).exists())

        self.assertFalse(IterableFieldModel.objects.exclude(set_field__isempty=False).exists())
        self.assertTrue(IterableFieldModel.objects.exclude(set_field__isempty=True).exists())

    def test_exclude_contains(self):
        IterableFieldModel.objects.create(list_field=["apples", "bananas"])
        IterableFieldModel.objects.create(list_field=["apples", "pears"])

        self.assertRaises(
            NotSupportedError, list,
            IterableFieldModel.objects.exclude(
                list_field__contains="bananas"
            ).order_by("list_field")
        )

        self.assertRaises(
            NotSupportedError, list,
            IterableFieldModel.objects.exclude(
                list_field__contains="pears"
            ).order_by("list_field"),
        )

    def test_serialization(self):
        dt = datetime.datetime(2017, 1, 1, 12)
        instance = IterableFieldModel.objects.create(
            set_field={u"foo"},
            list_field=[u"bar"],
            set_field_int={123},
            list_field_int=[456],
            set_field_dt={dt},
            list_field_dt=[dt],
        )

        self.assertEqual("['foo']", instance._meta.get_field("set_field").value_to_string(instance))
        self.assertEqual("['bar']", instance._meta.get_field("list_field").value_to_string(instance))
        self.assertEqual("[123]", instance._meta.get_field("set_field_int").value_to_string(instance))
        self.assertEqual("[456]", instance._meta.get_field("list_field_int").value_to_string(instance))
        self.assertEqual("['2017-01-01T12:00:00']", instance._meta.get_field("set_field_dt").value_to_string(instance))
        self.assertEqual("['2017-01-01T12:00:00']", instance._meta.get_field("list_field_dt").value_to_string(instance))

    def test_saving_forms(self):
        class TestForm(forms.ModelForm):
            class Meta:
                model = IterableFieldModel
                fields = ("set_field", "list_field")

        post_data = {"set_field": ["1", "2"], "list_field": ["1", "2"]}

        form = TestForm(post_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_cannot_have_min_length_and_blank(self):
        """ Having min_length=X, blank=True doesn't make any sense, especially when you consider
            that django will skip the min_length check when the value (list/set)is empty.
        """
        self.assertRaises(ImproperlyConfigured, ListField, CharField(max_length=100), min_length=1, blank=True)
        self.assertRaises(ImproperlyConfigured, SetField, CharField(max_length=100), min_length=1, blank=True)

    def test_list_field_set_field_min_max_lengths_valid(self):
        """ Test that when the min_legnth and max_length of a ListField and SetField are correct
            that no validation error is rasied.
        """
        others = []
        for x in range(2):
            others.append(IterableIterableRelatedModel.objects.create())
        instance = IterableIterableFieldsWithValidatorsModel(
            related_set=set(others),  # not being tested here
            related_list=others,  # not being tested here
            set_field=set(["1", "2"]),
            list_field=["1", "2"],
        )
        instance.full_clean()

    def test_list_field_max_length_invalid(self):
        others = []
        for x in range(2):
            others.append(IterableIterableRelatedModel.objects.create())
        instance = IterableIterableFieldsWithValidatorsModel(
            related_set=set(others),  # not being tested here
            related_list=others,  # not being tested here
            set_field=set(["1", "2"]),  # not being tested here
            list_field=["1", "2", "3", "4", "5"],
        )
        self.assertRaisesMessage(
            ValidationError,
            "{'list_field': ['Ensure this field has at most 3 items (it has 5).']}",
            instance.full_clean,
        )

    def test_list_field_min_length_invalid(self):
        others = []
        for x in range(2):
            others.append(IterableIterableRelatedModel.objects.create())
        instance = IterableIterableFieldsWithValidatorsModel(
            related_set=set(others),  # not being tested here
            related_list=others,  # not being tested here
            set_field=set(["1", "2"]),  # not being tested here
            list_field=["1"],
        )
        self.assertRaisesMessage(
            ValidationError,
            "{'list_field': ['Ensure this field has at least 2 items (it has 1).']}",
            instance.full_clean,
        )

    def test_set_field_max_length_invalid(self):
        others = []
        for x in range(2):
            others.append(IterableIterableRelatedModel.objects.create())
        instance = IterableIterableFieldsWithValidatorsModel(
            related_set=set(others),  # not being tested here
            related_list=others,  # not being tested here
            list_field=["1", "2"],  # not being tested here
            set_field=set(["1", "2", "3", "4", "5"]),
        )
        self.assertRaisesMessage(
            ValidationError, "{'set_field': ['Ensure this field has at most 3 items (it has 5).']}", instance.full_clean
        )

    def test_set_field_min_length_invalid(self):
        others = []
        for x in range(2):
            others.append(IterableIterableRelatedModel.objects.create())
        instance = IterableIterableFieldsWithValidatorsModel(
            related_set=set(others),  # not being tested here
            related_list=others,  # not being tested here
            list_field=["1", "2"],  # not being tested here
            set_field=set(["1"]),
        )
        self.assertRaisesMessage(
            ValidationError,
            "{'set_field': ['Ensure this field has at least 2 items (it has 1).']}",
            instance.full_clean,
        )

    def test_list_field_serializes_and_deserializes(self):
        obj = IterableFieldModel(list_field=["foo", "bar"])
        data = serializers.serialize("json", [obj])

        new_obj = next(serializers.deserialize("json", data)).object
        self.assertEqual(new_obj.list_field, ["foo", "bar"])

    def test_set_field_serializes_and_deserializes(self):
        obj = IterableFieldModel(set_field=set(["foo", "bar"]))
        data = serializers.serialize("json", [obj])

        new_obj = next(serializers.deserialize("json", data)).object
        self.assertEqual(new_obj.set_field, set(["foo", "bar"]))
