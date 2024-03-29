# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from easyrequest_hay_app import views


admin.autodiscover()


urlpatterns = [

    url( r'^admin/', admin.site.urls ),  # eg host/project_x/admin/

    url( r'^bul_search/$', views.bul_search, name='bul_search_url' ),

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^confirm/$', views.confirm, name='confirm_url' ),

    url( r'^confirm_handler/$', views.confirm_handler, name='confirm_handler_url' ),

    url( r'^problem/$', views.problem, name='problem_url' ),

    url( r'^shib_login/$', views.shib_login, name='shib_login_url' ),

    url( r'^shib_login_handler/$', views.shib_login_handler, name='shib_login_handler_url' ),

    url( r'^processor/$', views.processor, name='processor_url' ),
    url( r'^alma_processor/$', views.alma_processor, name='alma_processor_url' ),

    url( r'^stats_api/$', views.stats, name='stats_url' ),

    ## helpers
    url( r'^version/$', views.version, name='version_url' ),
    url( r'^error_check/$', views.error_check, name='error_check_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ]
