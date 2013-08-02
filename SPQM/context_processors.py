from datetime import timedelta
from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils import timezone
from SPQM.frontend import forms
from SPQM.frontend.models import Person, Category

register_form = forms.RegisterUserForm
login_form = forms.LoginUserForm


def global_vars(request):
    """
    Adds global variables to the context.
    """
    global register_form, login_form
    temp_register_form = register_form
    temp_login_form = login_form
    # Restore values
    register_form = forms.RegisterUserForm
    login_form = forms.LoginUserForm

    persons = Person.objects.all()
    number_of_persons = len(persons)
    start_date = timezone.now().date()

    return {
        # Constants
        'SITE_NAME': settings.SITE_NAME,
        'current_url': resolve(request.path_info).url_name,

        # Variables
        'number_of_persons': number_of_persons,
        'persons_added_today': len(
            Person.objects.filter(date_added__range=(start_date, start_date + timedelta(days=1)))
        ),
        'percent_of_politicians': round(
            len(Person.objects.filter(category=Category.objects.get(en_name='Politician'))) * 100.0 / number_of_persons, 2
        ),
        'world_corruption': 99.98,
        'register_form': temp_register_form,
        'login_form': temp_login_form
    }