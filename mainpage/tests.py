from django.test import TestCase
from .models import Country, Locality, Meansoftransport, Routes, Waypoints, Permit, Client, Sellpermit
from django.contrib.auth import get_user_model, authenticate
from datetime import datetime

User = get_user_model()


class CountryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name='Америка', need_for_a_visa=True, need_a_passport=True, visa_cost=890, pas_cost=890)
        Country.objects.create(name='Америка2', need_for_a_visa=True, need_a_passport=False, visa_cost=0, pas_cost=0)

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
        expected_object_need_for_a_visa = country.need_for_a_visa
        self.assertEquals(expected_object_need_for_a_visa, True)
        field_label = country._meta.get_field('visa_cost').verbose_name
        self.assertEquals(field_label, 'Стоимость визы')
        expected_object_visa_cost = country.visa_cost
        self.assertEquals(expected_object_visa_cost, 890)

    def test_passp(self):
        country = Country.objects.get(id=2)
        field_label = country._meta.get_field('need_a_passport').verbose_name
        self.assertEquals(field_label, 'Обязательность загранпаспорта')
        expected_object_need_a_passport = country.need_a_passport
        self.assertEquals(expected_object_need_a_passport, False)
        field_label = country._meta.get_field('pas_cost').verbose_name
        self.assertEquals(field_label, 'Стоимость загранпаспорта')
        expected_object_pas_cost = country.pas_cost
        self.assertEquals(expected_object_pas_cost, 0)


class LocalityModelTest(TestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Америка', need_for_a_visa=True, need_a_passport=True,
                                              visa_cost=890, pas_cost=890)
        self.locality = Locality.objects.create(name='Gtrby', country_id=self.country)

    def test_locality(self):
        self.assertEqual(self.country.name, 'Америка')
        self.assertEqual(self.country.visa_cost, 890)
        self.assertEqual(self.country.pas_cost, 890)
        self.assertEqual(self.country.need_for_a_visa, True)
        self.assertEqual(self.country.need_a_passport, True)
        self.assertEqual(self.locality.name, 'Gtrby')
        self.assertEqual(self.locality.country_id, self.country)


class MeansoftransportModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Meansoftransport.objects.create(name='Тарелка')
        Meansoftransport.objects.create(name='Велосипед')

    def test_transport(self):
        meansoftransport = Meansoftransport.objects.get(id=1)
        field_label = meansoftransport._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Транспорт')
        max_length = meansoftransport._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)
        expected_object_meansoftransport = meansoftransport.name
        self.assertEquals(expected_object_meansoftransport, str(meansoftransport))
        meansoftransport = Meansoftransport.objects.get(id=2)
        expected_object_meansoftransport = meansoftransport.name
        self.assertEquals(expected_object_meansoftransport, str(meansoftransport))


class UsersTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser1', password='qwerty123qwerty')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='testuser1', password='qwerty123qwerty')
        self.assertTrue(user is not None and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='test', password='qwerty123qwerty')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='testuser1', password='23qwerty')
        self.assertFalse(user is not None and user.is_authenticated)


class RoutesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.routes = Routes.objects.create(name='Сколько у тебя ещё классов?', description='Серьезно? нот нулл?', active=True)

    def test_routes(self):
        routes = Routes.objects.get()
        field_label = routes._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Маршрут')
        max_length = routes._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)
        expected_object_routes = routes.name
        self.assertEquals(expected_object_routes, str(routes))
        expected_object_active = routes.active
        self.assertEquals(expected_object_active, True)

    def tearDown(self):
        self.routes.delete()


class WaypointsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.country = Country.objects.create(name='Америка3', need_for_a_visa=True, need_a_passport=True,
                                             visa_cost=1000, pas_cost=100)
        cls.l1 = Locality.objects.create(name='Gtrby', country_id=cls.country)
        cls.m1 = Meansoftransport.objects.create(name='Тарелка')
        cls.r1 = Routes.objects.create(name='Сколько у тебя ещё классов?',
                                       description='Серьезно? нот нулл?', active=True)
        cls.waypoints = Waypoints.objects.create(locality_id=cls.l1, route_point_number=1, means_of_transport_id=cls.m1,
                                                 hotel='Оверлук',hotel_class=5,
                                                 hotel_description='Горы, снег. Лабиринта рядом с отелем нет',
                                                 excursions='No', routes_id=cls.r1)
        Waypoints.objects.create(locality_id=cls.l1, route_point_number=2, means_of_transport_id=cls.m1,
                                 hotel='Оверлук2', hotel_class=5, hotel_description='Горы. Лабиринт рядом с отелем',
                                 excursions='Not', routes_id=cls.r1)

    def test_waypoints(self):
        waypoints = Waypoints.objects.get(id=1)
        field_label = waypoints._meta.get_field('hotel').verbose_name
        self.assertEquals(field_label, 'Отель')
        max_length = waypoints._meta.get_field('hotel').max_length
        self.assertEquals(max_length, 255)

    def test_that_reads_hotel_from_db(self):
        db_hotel = Waypoints.objects.get(id=2).hotel
        assert db_hotel == "Оверлук2"

    def test_that_changes_hotel(self):
        self.waypoints.hotel = "Overlyk"

    def tearDown(self):
        self.waypoints.delete()


class PermitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.r1 = Routes.objects.create(name='Сколько у тебя ещё классов?',
                                       description='Серьезно? нот нулл?', active=True)
        cls.permit = Permit.objects.create(name='ТестПутёвка1', description='ВАу!!! описание лучшая вещь..',
                                           price=12000, begin_date=datetime(2017, 1, 1, 1, 1, 1),
                                           end_date=datetime(2017, 1, 1, 1, 1, 1), route_id=cls.r1, active=True)

    def test_permit(self):
        permit = Permit.objects.get()
        field_label = permit._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')
        max_length = permit._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test_that_changes_name(self):
        self.permit.name = "ТестПутёвка2"

    def test_that_reads_name_from_db(self):
        db_name = Permit.objects.get().name
        assert db_name == "ТестПутёвка1"

    def tearDown(self):
        self.permit.delete()


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client.objects.create(surname='столько', name='полей', patronymic='вау', phone='+71234567765',
                                           registedate=datetime(2017, 1, 1, 1, 1, 1),
                                           passport='1234567', zagranpassport='1234567')

    def test_that_changes_surname(self):
        self.client.surname = "Фамилия"

    def test_that_reads_surname_from_db(self):
        db_surname = Client.objects.get().surname
        assert db_surname == "столько"

    def test_client(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Имя')
        max_length = client._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)
        expected_object_client = '{} {} {} {}' .format(client.surname, client.name, client.patronymic, client.phone)
        self.assertEquals(expected_object_client, str(client))


class SellpermitModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='testuser1', password='qwerty123qwerty')
        cls.r1 = Routes.objects.create(name='Сколько у тебя ещё классов?',
                                       description='Серьезно? нот нулл?', active=True)
        cls.permit = Permit.objects.create(name='ТестПутёвка1', description='ВАу!!! описание лучшая вещь..',
                                           price=12000, begin_date=datetime(2017, 1, 1, 1, 1, 1),
                                           end_date=datetime(2017, 1, 1, 1, 1, 1), route_id=cls.r1, active=True)
        cls.client = Client.objects.create(surname='столько', name='полей', patronymic='вау', phone='+71234567765',
                                           registedate=datetime(2017, 1, 1, 1, 1, 1),
                                           passport='1234567', zagranpassport='1234567')
        cls.sellpermit = Sellpermit.objects.create(permit_id=cls.permit, date_time_sale=datetime(2019, 1, 3, 1, 1, 1),
                                                   price=12, discount=50, price_disc=6, user_id=cls.user,
                                                   client_id=cls.client)

    def test_that_changes_discount(self):
        self.sellpermit.discount = 70

    def test_that_reads_discount_from_db(self):
        db_sellpermit = Sellpermit.objects.get().discount
        assert db_sellpermit == 50

    def test_sellpermit(self):
        sellpermit = Sellpermit.objects.get()
        field_label = sellpermit._meta.get_field('permit_id').verbose_name
        self.assertEquals(field_label, 'Путёвка')

    def tearDown(self):
        self.sellpermit.delete()
