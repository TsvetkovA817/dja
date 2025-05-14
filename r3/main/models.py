# verbose_name - отображение в админке
# choices - выбор из предопределенных значений
# Meta класс - настройки
# метод `__str__` для отображения, добавил id

from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, verbose_name='Телефон')

    def __str__(self):
        return f'{self.id} {self.name} {self.middle_name} {self.last_name}'


GEARBOX_CHOICES = (
    ('manual', 'Механика'),
    ('automatic', 'Автомат'),
    ('вариатор', 'CVT'),
    ('robot', 'Робот')
)

FUEL_TYPE_CHOICES = (
    ('gasoline', 'Бензин'),
    ('diesel', 'Дизель'),
    ('hybrid', 'Гибрид'),
    ('electro', 'Электро')
)

BODY_TYPE_CHOICES = (
    ('sedan', 'Седан'),
    ('hatchback', 'Хэтчбек'),
    ('SUV', 'Внедорожник'),
    ('wagon', 'Универсал'),
    ('minivan', 'Минивэн'),
    ('pickup', 'Пикап'),
    ('coupe', 'Купе'),
    ('cabrio', 'Кабриолет')
)


DRIVE_UNIT_CHOICES = (
    ('rear', 'Задний'),
    ('front', 'Передний'),
    ('full', 'Полный')
)


class Car(models.Model):
    model = models.CharField(max_length=100, verbose_name='Модель авто')
    year = models.PositiveIntegerField(verbose_name='Год выпуска')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    mileage = models.PositiveIntegerField(verbose_name='Пробег')
    volume = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Объем двигателя')
    body_type = models.CharField(
        max_length=20,
        choices=BODY_TYPE_CHOICES,
        verbose_name='Тип кузова'
    )
    drive_unit = models.CharField(
        max_length=10,
        choices=DRIVE_UNIT_CHOICES,
        verbose_name='Привод'
    )
    gearbox = models.CharField(
        max_length=20,
        choices=GEARBOX_CHOICES,
        verbose_name='Коробка передач'
    )
    fuel_type = models.CharField(
        max_length=10,
        choices=FUEL_TYPE_CHOICES,
        verbose_name='Тип топлива'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    image = models.ImageField(
        upload_to='cars/',
        null=True,
        blank=True,
        verbose_name='Изображение авто'
    )

    def __str__(self):
        return f'{self.id} {self.model} {self.year} ({self.color})'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Sale(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Клиент'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name='Автомобиль'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата продажи'
    )

    def __str__(self):
        return f'Продажа #{self.id} - {self.car} клиенту {self.client}'

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        ordering = ['-created_at']
