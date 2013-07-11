from datetime import datetime
from random import randint
from cities_light.models import City
from django.http import Http404
from django.shortcuts import redirect

from django.utils import crypto, timezone
from django.views import generic as generic_views
from SPQM.frontend import forms

from SPQM.frontend.models import Category, Person, Information


class HomeView(generic_views.FormView):
    template_name = 'frontend/home.html'
    form_class = forms.RegisterUserForm

    def get(self, request, *args, **kwargs):
        # fill_db()
        return super(HomeView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        # TODO: User Login

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'persons': Person.objects.all()[:20],
        })
        return context


class PersonView(generic_views.TemplateView):
    template_name = 'frontend/person.html'

    def get(self, request, *args, **kwargs):
        person_name = kwargs['person_name'].split('_')
        if len(person_name) != 2:
            raise Http404

        person_id = -1
        if 'person_id' in kwargs:
            person_id = int(kwargs['person_id'])

        # First check if name is unique (name has an advantage to id)
        information = Information.objects.filter(first_name=person_name[0], last_name=person_name[1])
        if len(information) == 1:
            person = Person.objects.get(information=information)
            if person.id != person_id and person_id != -1:
                return redirect(person.create_url())
        # Else check id
        elif Person.objects.filter(id=person_id).exists():
            person = Person.objects.get(id=person_id)
            if person.information.first_name != person_name[0] or person.information.last_name != person_name[1]:
                return redirect(person.create_url())
        else:
            raise Http404
        request.session['person'] = person
        return super(PersonView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)
        context.update({
            'person': self.request.session['person'],
        })
        return context


def fill_db():
    # Create Categories
    category_names = ['Politician', 'Banker', ]
    category_desciptions = ['Bla bla bla bla', 'Bla bla bla bla', ]
    for i in range(0, len(category_names)):
        if not Category.objects.filter(en_name=category_names[i]).exists():
            Category(en_name=category_names[i], sl_name=category_names[i], description=category_desciptions[i]).save()
    # Create Persons
    description = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'

    for j in range(0, 20):
        city = 'city'  # City.objects.filter(country__name='United Kingdom').get(name='London')
        information = Information(
            first_name=crypto.get_random_string(5),
            last_name=crypto.get_random_string(5),
            birth_date=datetime(timezone.now().year + 100, timezone.now().month, 1),
            city=city,
            street='Dawning street 3'
        )
        information.save()
        Person(
            information=information,
            category=Category.objects.get(en_name=category_names[randint(0, len(category_names) - 1)]),
            description=description
        ).save()
