from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my_audits', views.my_audits, name='my_audits'),
    path('login_page', views.login_page, name='login_page'),
    path('register', views.register, name='register'),
    path('my_audits/<int:audit_id>', views.dynamic_audit_results, name='audit_results')
]