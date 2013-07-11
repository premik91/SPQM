from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import redirect

from django.views import generic as generic_views
from SPQM.frontend import forms

from SPQM.frontend.models import Person, Information
from SPQM import testing


class HomeView(generic_views.FormView):
    template_name = 'frontend/home.html'
    form_class = forms.RegisterUserForm

    def get(self, request, *args, **kwargs):
        # testing.fill_db()
        return super(HomeView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Load and send 4 more persons
        if request.is_ajax():
            number_of_persons = int(request.POST['number_of_persons'])
            json = serializers.serialize(
                'json',
                Person.objects.all()[number_of_persons:number_of_persons+4],
                indent=4,
                relations=('information',)
            )
            return HttpResponse(json)

        # TODO: User Login
        username = request.POST['username']

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'persons': Person.objects.all()[:4],
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
