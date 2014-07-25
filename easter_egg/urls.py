from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    'easter_egg',
    url(r'^$', 'views.index', name='index'),
    url(r'^test$', 'views.test', name='easter_egg_test'),
)
