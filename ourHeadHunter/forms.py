from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, forms
from django import forms
from ourHeadHunter.models import Person, Company, User, Vacancy, Category, Response


class UserPersonCreationForm(ModelForm):
    class Meta:
        model = Person
        fields = ('surname', 'first_name', 'second_name', 'date_of_birth', 'about')


class UserCompanyCreationForm(ModelForm):
    class Meta:
        model = Company
        fields = ('company_name', 'address', 'about')


class UserWithTypesCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')


class VacancyCreationForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ('vacancy_name', 'salary', 'category', 'description')


class FilterForm(forms.Form):
    TEST_CHOICES_CATEGORY = [[x.id, x.category_name] for x in Category.objects.all()]
    category = forms.MultipleChoiceField(choices=TEST_CHOICES_CATEGORY, widget=forms.CheckboxSelectMultiple,
                                         required=False, label='Категория')

    TEST_CHOICES_COMPANY = [[x.id, x.company_name] for x in Company.objects.all()]
    company = forms.MultipleChoiceField(choices=TEST_CHOICES_COMPANY, widget=forms.CheckboxSelectMultiple,
                                        required=False, label='Компания')


class ResponseCreationForm(ModelForm):
    class Meta:
        model = Response
        fields = ['message']
