from django.conf.urls import patterns, url
from frontend import views as frontend_views

urlpatterns = patterns(
    '',
    url(r'^$', frontend_views.HomeView.as_view(), name='home'),

    # User account
    url(r'^logout/$', frontend_views.LogoutView.as_view(), name='logout'),
    
    # Person page
    url(r'^(?P<person_name>\w+)-(?P<person_id>\d+)/$', frontend_views.PersonView.as_view(), name='person'),
    url(r'^(?P<person_name>\w+)/$', frontend_views.PersonView.as_view(), name='person_name'),
)
