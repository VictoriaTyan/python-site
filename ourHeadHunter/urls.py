from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('ourHeadHunter/$', views.main_view, name='main'),
    url('ourHeadHunter/logout/$', views.log_out, name='logout'),
    url('ourHeadHunter/main_person/logout/$', views.log_out, name='logout'),  # TODO!
    url('ourHeadHunter/main_company/logout/$', views.log_out, name='logout'),
    url('ourHeadHunter/main_company/summary_list/logout$', views.log_out, name='logout'),
    url('ourHeadHunter/main_company/company_responses/logout$', views.log_out, name='logout'),
    url('ourHeadHunter/main_person/vacancies_list/logout$', views.log_out, name='logout'),
    url('ourHeadHunter/main_person/person_responses/logout$', views.log_out, name='logout'),
    url('ourHeadHunter/main_person/vacancies_list/response_person/logout$', views.log_out, name='logout'),
    url('ourHeadHunter/main_company/summary_list/response_company/logout$', views.log_out, name='logout'),
    url('ourHeadHunter/login/$', views.log_in, name='login'),
    url('ourHeadHunter/register/$', views.register, name='register'),
    url('ourHeadHunter/register/register_person/$', views.register_person, name='register_person'),
    url('ourHeadHunter/register/register_company/$', views.register_company, name='register_company'),
    url('ourHeadHunter/main_person/$', views.main_person, name='main_person'),
    url('ourHeadHunter/main_company/$', views.main_company, name='main_company'),
    url('ourHeadHunter/main_company/add_vacancy/$', views.add_vacancy, name='add_vacancy'),
    url('ourHeadHunter/main_person/vacancies_list/response_person/$', views.vacancies_list, name='vacancies_list'),
    url('ourHeadHunter/main_company/summary_list/response_company/$', views.summary_list, name='summary_list'),
    path('ourHeadHunter/main_company/edit_vacancy/<int:vac_id>/', views.edit_vacancy, name='edit_vacancy'),
    path('ourHeadHunter/main_company/delete_vacancy/<int:vac_id>/', views.delete_vacancy, name='delete_vacancy'),
    path('ourHeadHunter/main_company/delete_vacancy/<int:vac_id>/confirm_delete/', views.confirm_delete, name='confirm_delete'),
    path('ourHeadHunter/main_company/summary_list/', views.summary_list, name='summary_list'),
    path('ourHeadHunter/main_person/vacancies_list/', views.vacancies_list, name='vacancies_list'),
    path('ourHeadHunter/main_person/vacancies_list/response_person/<int:vac_id>/', views.response_person, name='response_person'),
    path('ourHeadHunter/main_company/company_responses/', views.company_responses, name='company_responses'),
    path('ourHeadHunter/main_company/summary_list/response_company/<int:pers_id>/', views.response_company, name='response_company'),
    path('ourHeadHunter/main_person/person_responses/', views.person_responses, name='person_responses'),
    path('ourHeadHunter/main_company/company_responses/person_info/<int:res_id>/', views.person_info, name='person_info'),
    path('ourHeadHunter/main_person/person_responses/company_info/<int:res_id>/', views.company_info, name='company_info'),
]

"""  
"""
