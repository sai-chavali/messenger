"""accounts urls."""

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [


    path('register/', views.RegistrationView.as_view(), name='register'),

    url(r'^login/$', auth_views.login,
        {'template_name': 'accounts/login.html'}, name='login'),

    url(r'^logout/$', auth_views.logout,
        {'template_name': 'accounts/logout.html'}, name='logout'),

    url(r'^password_change/$', auth_views.password_change,
        {'template_name': 'accounts/password_change_form.html'},
        name='password_change'),

    url(r'^password_change/done/$', auth_views.password_change_done,
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done'),

    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'accounts/password_reset_form.html'},
        name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'accounts/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password_reset_complete'),
]
