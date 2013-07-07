from django.conf.urls import patterns, url
from frontend import views as frontend_views

urlpatterns = patterns(
    '',
    url(r'^$', frontend_views.HomeView.as_view(), name='home'),
)
