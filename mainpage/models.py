from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    need_for_a_visa = models.BooleanField(default=False, verbose_name='Обязательность визы')
    need_a_passport = models.BooleanField(default=False, verbose_name='Обязательность загранпаспорта')
    visa_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость визы')
    pas_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость загранпаспорта')

    class Meta:
        verbose_name = 'Страны'
        verbose_name_plural = 'Страны'


class Locality(models.Model):
    name = models.CharField(max_length=255, verbose_name='Город')
    country_id = models.ForeignKey('Country', on_delete=models.DO_NOTHING, verbose_name='Страна')

    def __str__(self):
        return 'Страна: {} - Город: {}'.format(self.country_id.name, self.name)

    class Meta:
        verbose_name = 'Населённые пункты'
        verbose_name_plural = 'Населённые пункты'


class Meansoftransport(models.Model):
    name = models.CharField(max_length=255, verbose_name='Транспорт')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Виды транспорта'
        verbose_name_plural = 'Виды транспорта'


class Routes(models.Model):
    name = models.CharField(max_length=255, verbose_name='Маршрут')
    description = models.TextField(verbose_name='Описание')
    active = models.BooleanField(default=True, verbose_name='Есть ли в наличии?')

    class Meta:
        verbose_name = 'Маршруты'
        verbose_name_plural = 'Маршруты'


class Waypoints(models.Model):
    STAR_CHECKLIST = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    locality_id = models.ForeignKey('Locality', on_delete=models.DO_NOTHING, verbose_name='Населённый пункт')
    route_point_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                             default=1, verbose_name='Номер точки в маршруте')
    means_of_transport_id = models.ForeignKey('Meansoftransport', on_delete=models.DO_NOTHING,
                                              verbose_name='Вид транспорта')
    hotel = models.CharField(max_length=255, verbose_name='Отель')
    hotel_class = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], choices=STAR_CHECKLIST,
                                      verbose_name='Звёзды')
    hotel_description = models.TextField(verbose_name='Описание')
    excursions = models.TextField(verbose_name='Экскурсии')
    routes_id = models.ForeignKey('Routes', on_delete=models.DO_NOTHING, verbose_name='Маршрут')

    def __str__(self):
        return 'Населённый пункт: {} - Номер точки в маршруте: {} - Вид транспорта: {}'\
            .format(self.locality_id.name, self.route_point_number, self.means_of_transport_id.name)

    class Meta:
        verbose_name = 'Точки маршрута'
        verbose_name_plural = 'Точки маршрута'


class Permit(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    begin_date = models.DateField(verbose_name='Дата начала путёвки')
    end_date = models.DateField(verbose_name='Дата окончания путёвки')
    route_id = models.ForeignKey('Routes', on_delete=models.DO_NOTHING, verbose_name='Маршрут')
    active = models.BooleanField(default=True, verbose_name='Активна ли?')

    class Meta:
        verbose_name = 'Путёвки'
        verbose_name_plural = 'Путёвки'


class Client(models.Model):
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    phone = PhoneNumberField(verbose_name='Номер телефона')
    registedate = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    passport = models.CharField(max_length=255, verbose_name='Данные паспорта')
    zagranpassport = models.CharField(max_length=255, verbose_name='Данные загранпаспорта')

    class Meta:
        verbose_name = 'Клиенты'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']


class Sellpermit(models.Model):
    permit_id = models.ForeignKey('Permit', on_delete=models.DO_NOTHING, verbose_name='Путёвка')
    date_time_sale = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время продажи')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость', null=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   default=0, verbose_name='Скидка?')
    price_disc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена со скидкой', null=True)
    user_id = models.ForeignKey(User, verbose_name='Агент', on_delete=models.DO_NOTHING)
    client_id = models.ForeignKey('Client', on_delete=models.DO_NOTHING, verbose_name='Клиент')

    def __str__(self):
        return 'Путёвка: {}. Дата и время продажи: {}. Цена со скидкой: {}. Клиент: {}.'\
            .format(self.permit_id.name, self.date_time_sale, self.price_disc, self.client_id.name)

    def save(self):
        self.price = self.permit_id.price
        self.price_disc = self.permit_id.price - self.permit_id.price * self.discount/100
        super().save()

    class Meta:
        verbose_name = 'Список продаж'
        verbose_name_plural = 'Список продаж'
