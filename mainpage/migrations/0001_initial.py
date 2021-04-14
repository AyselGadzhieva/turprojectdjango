# Generated by Django 3.2 on 2021-04-14 06:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('registedate', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('passport', models.CharField(max_length=255, verbose_name='Данные паспорта')),
                ('zagranpassport', models.CharField(max_length=255, verbose_name='Данные загранпаспорта')),
            ],
            options={
                'verbose_name': 'Клиенты',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('need_for_a_visa', models.BooleanField(default=False, verbose_name='Обязательность визы')),
                ('need_a_passport', models.BooleanField(default=False, verbose_name='Обязательность загранпаспорта')),
                ('visa_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость визы')),
                ('pas_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость загранпаспорта')),
            ],
            options={
                'verbose_name': 'Страны',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Город')),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Населённые пункты',
                'verbose_name_plural': 'Населённые пункты',
            },
        ),
        migrations.CreateModel(
            name='Meansoftransport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Транспорт')),
            ],
            options={
                'verbose_name': 'Виды транспорта',
                'verbose_name_plural': 'Виды транспорта',
            },
        ),
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('begin_date', models.DateField(verbose_name='Дата начала путёвки')),
                ('end_date', models.DateField(verbose_name='Дата окончания путёвки')),
                ('active', models.BooleanField(default=True, verbose_name='Активна ли?')),
            ],
            options={
                'verbose_name': 'Путёвки',
                'verbose_name_plural': 'Путёвки',
            },
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Маршрут')),
                ('description', models.TextField(verbose_name='Описание')),
                ('active', models.BooleanField(default=True, verbose_name='Есть ли в наличии?')),
            ],
            options={
                'verbose_name': 'Маршруты',
                'verbose_name_plural': 'Маршруты',
            },
        ),
        migrations.CreateModel(
            name='Waypoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_point_number', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Номер точки в маршруте')),
                ('hotel', models.CharField(max_length=255, verbose_name='Отель')),
                ('hotel_class', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Звёзды')),
                ('hotel_description', models.TextField(verbose_name='Описание')),
                ('excursions', models.TextField(verbose_name='Экскурсии')),
                ('locality_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.locality', verbose_name='Населённый пункт')),
                ('means_of_transport_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.meansoftransport', verbose_name='Вид транспорта')),
                ('routes_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.routes', verbose_name='Маршрут')),
            ],
            options={
                'verbose_name': 'Точки маршрута',
                'verbose_name_plural': 'Точки маршрута',
            },
        ),
        migrations.CreateModel(
            name='Sellpermit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_sale', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время продажи')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Стоимость')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Скидка?')),
                ('price_disc', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Цена со скидкой')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.client', verbose_name='Клиент')),
                ('permit_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.permit', verbose_name='Путёвка')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Агент')),
            ],
            options={
                'verbose_name': 'Список продаж',
                'verbose_name_plural': 'Список продаж',
            },
        ),
        migrations.AddField(
            model_name='permit',
            name='route_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mainpage.routes', verbose_name='Маршрут'),
        ),
    ]
