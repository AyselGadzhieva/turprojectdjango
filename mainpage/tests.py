from django.test import TestCase
from .models import Country, Locality, Meansoftransport, Routes, Waypoints, Permit, Client, Sellpermit
from django.contrib.auth import get_user_model


User = get_user_model()


class CountryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name='Америка', need_for_a_visa=True, need_a_passport=True, visa_cost=890, pas_cost=890)
        Country.objects.create(name='Америка2', need_for_a_visa=True, need_a_passport=False, visa_cost=0, pas_cost=0)
        Country.objects.create(name='Америка3', need_for_a_visa=False, need_a_passport=False,
                               visa_cost=5890, pas_cost=5890)

    def test_name(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')
        max_length = country._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)
        expected_object_name = country.name
        self.assertEquals(expected_object_name, str(country))
        country = Country.objects.get(id=2)
        expected_object_name = country.name
        self.assertEquals(expected_object_name, str(country))


    def test_visa(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('need_for_a_visa').verbose_name
        self.assertEquals(field_label, 'Обязательность визы')
        expected_object_name = country.need_for_a_visa
        self.assertEquals(expected_object_name, True)


class LocalityModelTest(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Америка', need_for_a_visa=True, need_a_passport=True,
                                              visa_cost=890, pas_cost=890)
        self.locality = Locality.objects.create(name='Gtrby', country_id=self.country)

    def test_change(self):
        self.assertEqual(self.country.name, 'Америка')
        self.assertEqual(self.country.visa_cost, 890)
        self.assertEqual(self.country.pas_cost, 890)
        self.assertEqual(self.country.need_for_a_visa, True)
        self.assertEqual(self.country.need_a_passport, True)
        self.assertEqual(self.locality.name, 'Gtrby')
        self.assertEqual(self.locality.country_id, self.country)
