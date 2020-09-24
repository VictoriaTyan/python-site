from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLES = (
    ('person', 'Соискатель'),
    ('company', 'Работодатель')
)


class User(AbstractUser):
    role = models.CharField(choices=ROLES, max_length=50, verbose_name='Тип пользователя')
    pass


class Person(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    second_name = models.CharField(max_length=50, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    about = models.TextField(blank=True, null=True, verbose_name='О себе')

    def __str__(self):
        return self.surname + " " + self.first_name + " " + self.second_name


class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    about = models.TextField(blank=True, null=True, verbose_name='О компании')

    def __str__(self):
        return self.company_name


class Category(models.Model):
    category_name = models.CharField(max_length=200, verbose_name='Название категории')

    def __str__(self):
        return self.category_name


class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    vacancy_name = models.CharField(max_length=200, verbose_name='Заголовок')
    salary = models.PositiveIntegerField(blank=True, null=True, verbose_name='З/п')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, verbose_name='Категория')

    def __str__(self):
        return self.vacancy_name


class Response(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='Соискатель')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name='Вакансия')
    message = models.TextField(null=True, blank=True, verbose_name='Сообщение')
    to_company = models.BooleanField(null=True, blank=True, verbose_name='Откликнуться на вакансию от компании')


    def __str__(self):
        return self.vacancy.vacancy_name + " " + self.company.company_name + " " + self.person.first_name + " " \
               + self.person.second_name + " " + self.person.surname
