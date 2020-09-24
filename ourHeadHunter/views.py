from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import FilterForm, ResponseCreationForm
# Create your views here.
from ourHeadHunter.models import User, Person, Company, Vacancy, Response

from ourHeadHunter.forms import UserWithTypesCreationForm, UserPersonCreationForm, UserCompanyCreationForm, \
    VacancyCreationForm


class MainView(TemplateView):
    template_name = 'start_page.html'

    def get(self, request, **kwargs):
        ctx = {}
        if request.user.is_authenticated:
            if request.user.role == 'person':
                vacancies = Vacancy.objects.all()  # Vacancies
                ctx['vacancies'] = vacancies
            else:
                people = Person.objects.all()
                ctx['people'] = people
        return render(request, self.template_name, ctx)


def main_view(request):
    ctx = {}
    if request.user.is_authenticated:
        if request.user.role == 'person':
            return redirect('main_person')
        else:
            return redirect('main_company')
    else:
        return render(request, 'start_page.html', ctx)


def register(request):
    if request.method == 'POST':
        form = UserWithTypesCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            if form.cleaned_data['role'] == 'company':
                return redirect('register_company')
            else:
                return redirect('register_person')
    else:
        form = UserWithTypesCreationForm()
    return render(request, 'register.html', {'form': form})


def register_person(request):
    if request.method == 'POST':
        form = UserPersonCreationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.save()
            return redirect('main_person')
    else:
        form = UserPersonCreationForm()
    return render(request, 'register_person.html', {'form': form})


def register_company(request):
    if request.method == 'POST':
        form = UserCompanyCreationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.save()
            return redirect('main_company')
    else:
        form = UserCompanyCreationForm()
    return render(request, 'register_company.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.user = user
            if user.role == 'company':
                return redirect('main_company')
            else:
                return redirect('main_person')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('main')


def get_person(user):
    for person in Person.objects.all():
        if person.user == user:
            return person
    return None


def main_person(request):
    ctx = {}
    person = get_person(request.user)
    if request.method == "GET":
        if request.user.is_authenticated:
            ctx['person'] = person
    else:
        main_person(request)
    return render(request, 'main_person.html', ctx)


def get_company(user):
    for company in Company.objects.all():
        if company.user == user:
            return company
    return None


def get_company_vacancies(user):
    vacancies = []
    for vacancy in Vacancy.objects.all():
        if vacancy.company.user == user:
            vacancies.append(vacancy)
    return vacancies


def main_company(request):
    ctx = {}
    company = get_company(request.user)
    if request.method == "GET":
        if request.user.is_authenticated:
            vacancies = get_company_vacancies(request.user)
            ctx['vacancies'] = vacancies
            ctx['company'] = company
    else:
        main_company(request)
    return render(request, 'main_company.html', ctx)


def add_vacancy(request):
    if request.method == 'POST':
        form = VacancyCreationForm(request.POST)
        if form.is_valid():
            vac = form.save(commit=False)
            vac.company = get_company(request.user)
            if not vac.description:
                vac.description = ""
            vac.save()
            return redirect('main_company')
    else:
        form = VacancyCreationForm()
    return render(request, 'add_vacancy.html', {'form': form})


def edit_vacancy(request, vac_id):
    vac = get_object_or_404(Vacancy, id=vac_id)
    if request.method == 'POST':
        form = VacancyCreationForm(request.POST, instance=vac)
        if form.is_valid():
            vac = form.save(commit=False)
            vac.company = get_company(request.user)
            if not vac.description:
                vac.description = ""
            vac.save()
            return redirect('main_company')
    else:
        form = VacancyCreationForm(instance=vac)
    return render(request, 'edit_vacancy.html', {'form': form})


def delete_vacancy(request, vac_id):
    ctx = {}
    if request.method == 'GET':
        if request.user.is_authenticated:
            vacancy = get_object_or_404(Vacancy, id=vac_id)
            ctx['vacancy'] = vacancy
    else:
        delete_vacancy(request, vac_id)
    return render(request, 'delete_vacancy.html', ctx)


def confirm_delete(request, vac_id):
    if request.user.is_authenticated:
        vacancy = get_object_or_404(Vacancy, id=vac_id)
        vacancy.delete()
    return redirect('main_company')


def summary_list(request):
    ctx = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            resumes = Person.objects.all()
            ctx['resumes'] = resumes
    else:
        summary_list(request)
    return render(request, 'summary_list.html', ctx)


def vacancies_list(request):
    ctx = {}
    vacancies = Vacancy.objects.all()
    form = FilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['category']:
            vacancies = vacancies.filter(category__in=form.cleaned_data['category'])
        if form.cleaned_data['company']:
            vacancies = vacancies.filter(company__in=form.cleaned_data['company'])

    ctx['form'] = form
    ctx['vacancies'] = vacancies
    return render(request, 'vacancies_list.html', ctx)


def fill_response(res, request, info_id, is_to_company):
    res.to_company = is_to_company
    if res.to_company:
        vac = get_object_or_404(Vacancy, id=info_id)
        res.person = get_person(request.user)
        res.company = vac.company
        res.vacancy = vac
    else:
        vac = Vacancy.objects.first()
        resume = get_object_or_404(Person, id=info_id)
        res.company = get_company(request.user)
        res.person = resume
        res.vacancy = vac
    return res


def response_person(request, vac_id):
    vac = get_object_or_404(Vacancy, id=vac_id)
    if request.method == 'POST':
        form = ResponseCreationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res = fill_response(res, request, vac_id, True)
            if not res.message:
                res.message = ""
            res.save()
            return redirect('../..')
    else:
        form = ResponseCreationForm()
        form.vacancy = vac
    return render(request, 'response_person.html', {'form': form})


def response_company(request, pers_id):
    resume = get_object_or_404(Person, id=pers_id)
    if request.method == 'POST':
        form = ResponseCreationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res = fill_response(res, request, pers_id, False)
            if not res.message:
                res.message = ""
            res.save()
            return redirect('../..')
    else:
        form = ResponseCreationForm()
        form.person = resume
    return render(request, 'response_company.html', {'form': form})


def get_company_responses(user):
    result = []
    for resp in Response.objects.all():
        if resp.company.user == user and resp.to_company:
            result.append(resp)
    return result


def company_responses(request):
    ctx = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            responses = get_company_responses(request.user)
            ctx['responses'] = responses
    else:
        company_responses(request)
    return render(request, 'company_responses.html', ctx)


def get_person_responses(user):
    result = []
    for resp in Response.objects.all():
        if resp.person.user == user and not resp.to_company:
            result.append(resp)
    return result


def person_responses(request):
    ctx = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            responses = get_person_responses(request.user)
            ctx['responses'] = responses
    else:
        company_responses(request)
    return render(request, 'person_responces.html', ctx)


def person_info(request, res_id):
    ctx ={}
    if request.user.is_authenticated:
        response = get_object_or_404(Response, id=res_id)
        ctx['person'] = response.person
    return render(request, 'person_info.html', ctx)


def company_info(request, res_id):
    ctx = {}
    if request.user.is_authenticated:
        response = get_object_or_404(Response, id=res_id)
        ctx['company'] = response.company
    return render(request, 'company_info.html', ctx)