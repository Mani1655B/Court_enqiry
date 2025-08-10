from django.urls import path
from . import views

urlpatterns = [
    path('', views.case_query_form, name='case_query_form'),
]
