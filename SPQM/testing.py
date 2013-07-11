from datetime import datetime
from random import randint
from django.utils import crypto, timezone
from SPQM.frontend.models import Category, Information, Person
from cities_light.models import City


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