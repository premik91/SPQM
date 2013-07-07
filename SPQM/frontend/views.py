from datetime import datetime
from random import randint
from cities_light.models import City

from django.utils import crypto, timezone
from django.views import generic as generic_views

from SPQM.frontend.models import Category, Person, Information


class HomeView(generic_views.TemplateView):
    template_name = 'frontend/home.html'

    def get(self, request, *args, **kwargs):
        # fill_db()
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'persons': Person.objects.all(),
        })
        return context


def fill_db():
    # Fill Categories
    categories = []
    category_names = ['Politik', 'Tajkun', 'Bankir', ]
    category_desciptions = ['Bla bla bla bla', 'Bla bla bla bla', 'Bla bla bla bla', ]
    for i in range(0, len(category_names)-1):
        category = Category(en_name=category_names[i], sl_name=category_names[i], description=category_desciptions[i])
        category.save()
        categories.append(category.pk)

    # Create Persons
    description = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'

    for j in range(0, 20):
        city = City.objects.filter(country__name='United Kingdom').get(name='London')
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
            category=Category.objects.get(id=categories[randint(0, len(categories) - 1)]),
            description=description
        ).save()
