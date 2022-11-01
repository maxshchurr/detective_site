import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.urls import reverse


class Clients(models.Model):
    class Meta:
        db_table = 'clients'
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    phone_regex = RegexValidator(regex=r"\+\d{12}$",
                                 message='Phone number must be entered in this format +38(096)0351321. '
                                         'Up to 13 digits allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(verbose_name="Имя", max_length=70)

    tel_number = models.CharField(validators=[phone_regex], verbose_name="Телефон", max_length=15, unique=True)
    email = models.EmailField(verbose_name="Почта клиента", max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"{self.full_name}"


def validate_date_not_in_future(value):
    if value > datetime.date.today():
        raise ValidationError('date is in the future')


class Employees(models.Model):
    class Meta:
        db_table = 'agency_employees'
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ['salary']

    employees_status = (('Busy', 'Занят'),
                        ('Available', 'Свободен'))

    employees_position = (('Admin', 'Администратор'),
                          ('Chief', 'Начальник'),
                          ('Detective', 'Детектив'),
                          ('Assistant', 'Помощник детектива'),
                          ('Manager', 'Менеджер'))

    phone_regex = RegexValidator(regex=r"\+\d{12}$",
                                 message='Phone number must be entered in this format +380960351321. '
                                         'Up to 13 digits allowed.')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="Имя", max_length=30)
    surname = models.CharField(verbose_name="Фамилия", max_length=30)
    date_of_birth = models.DateField(verbose_name="Дата рождения", validators=[validate_date_not_in_future])
    e_email = models.EmailField(verbose_name="Почта", unique=True)
    # employees_password = models.CharField(verbose_name="Пароль", max_length=30)
    experience = models.IntegerField(validators=[MinValueValidator(1)], default=1, verbose_name="Стаж")
    salary = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(1)], default=10000,
                                 verbose_name="Зарплата")
    tel_number = models.CharField(validators=[phone_regex], verbose_name="Номер телефона сотрудника", max_length=13,
                                  unique=True)
    position = models.CharField(verbose_name="Должность", max_length=30, choices=employees_position)
    status = models.CharField(verbose_name="Статус сотрудника", max_length=30, default='Available',
                              choices=employees_status)
    chief = models.ForeignKey('self', verbose_name='Начальник', null=True, blank=True, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name} {self.surname} {self.position}'


class TypeOfOrder(models.Model):
    type_of_order = (
        ('Наблюдение', 'Наблюдение'),
        ('Сбор информации', 'Сбор информации'),
        ('Розыск человека', 'Розыск человека')
    )

    type = models.CharField(verbose_name='Тип заказа', max_length=50, choices=type_of_order, unique=True)
    price = models.IntegerField(verbose_name='Цена', validators=[MinValueValidator(1)], default=1000)
    expected_days = models.IntegerField(validators=[MinValueValidator(1)], default=1,
                                        verbose_name='Ожидаемое количество дней')

    class Meta:
        db_table = 'type_of_order'
        verbose_name = 'Тип заказа'
        verbose_name_plural = 'Типы заказов'

    def __str__(self):
        return f'{self.type}'


class Orders(models.Model):
    orders_status = (
        ('Closed', 'Закрыта'),
        ('In process', 'На рассмотрении менеджера'),
        ('Pending client', 'На рассмотрении клиента'),
        ('Payed', 'Оплачена'),
        ('Rejected by client', 'Отклонена клиентом'),
        ('Rejected by manager', 'Отклонена менеджером'),
        ('In work', 'В работе')
    )

    client_comment = models.TextField(verbose_name='Комментарий', max_length=250, null=False, blank=False)
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True, null=False)
    status = models.CharField(verbose_name='Статус заказа', choices=orders_status, max_length=50, default='In process',
                              null=False)
    rate = models.IntegerField(verbose_name='Рейтинг', default=1, null=True)
    type_of_order = models.ForeignKey(TypeOfOrder, verbose_name='Тип заказа', on_delete=models.PROTECT)
    client = models.ForeignKey(Clients, verbose_name='Клиент', on_delete=models.CASCADE)
    manager = models.ForeignKey(Employees, related_name='manager', verbose_name='Менеджер',
                                on_delete=models.CASCADE, null=True, blank=True)
    detective = models.ForeignKey(Employees, related_name='detective', verbose_name='Детектив',
                                  on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Id заказа: {self.pk}, Тип заказа: {self.type_of_order.type}, Цена: {self.type_of_order.price}, ' \
               f'Rate: {self.rate}, Клиент: {self.client.full_name}  Manger: {self.manager}'

    @property
    def get_full_price(self):
        return int(self.rate) * int(self.type_of_order.price)


class Tasks(models.Model):
    class Meta:
        db_table = 'tasks'
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    task_date = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    task_description = models.TextField(verbose_name='Описание задания', max_length=500, null=False, blank=False)
    employees = models.ForeignKey(Employees, verbose_name='Помощник детектива', on_delete=models.CASCADE, null=False)
    orders = models.ForeignKey(Orders, verbose_name='Заказ', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_description}'


class Assistant_comments(models.Model):
    class Meta:
        db_table = 'assistant_comments'
        verbose_name = 'Комментарий помощника'
        verbose_name_plural = 'Комментарии помощника'

    assistant_comments = models.TextField(verbose_name='Комментарий', max_length=500, null=False, blank=False)
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True, null=False)
    task = models.ForeignKey(Tasks, verbose_name='Задание', on_delete=models.CASCADE)
    employees = models.ForeignKey(Employees, verbose_name='Сотрудник', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.assistant_comments}'


class Report(models.Model):
    class Meta:
        db_table = 'report'
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'

    detective_report = models.TextField(verbose_name='Содержимое отчета', max_length=500, null=False, blank=False)
    report_date = models.DateField(verbose_name='Дата создания', auto_now_add=True, null=False)
    orders = models.OneToOneField(Orders, verbose_name='Заказ', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detective_report}'
