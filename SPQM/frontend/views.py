from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers, urlresolvers
from django.http import Http404, HttpResponse
from django.shortcuts import redirect

from django.views import generic as generic_views
from SPQM.frontend import forms

from SPQM.frontend.models import Person, Information
from SPQM import testing


class HomeView(generic_views.FormView):
    template_name = 'frontend/home.html'
    form_class = forms.RegisterUserForm
    success_url = urlresolvers.reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        # testing.fill_db()
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'persons': Person.objects.all()[:4],
        })
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)
        login(self.request, user)

        messages.success(self.request, 'You have successfully been registered. You will receive mail to confirm your email.')
        return super(HomeView, self).form_valid(form)

    def form_invalid(self, form):
        # Load and send 4 more persons
        if self.request.is_ajax():
            print 'ajax'
            number_of_persons = int(self.request.POST['number_of_persons'])
            json = serializers.serialize(
                'json',
                Person.objects.all()[number_of_persons:number_of_persons+4],
                indent=4,
                relations=('information', )
            )
            return HttpResponse(json)
        # If email is not in POST, than this is login
        elif 'email' not in self.request.POST:
            username = self.request.POST['username']
            password = self.request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(self.request, user)
                messages.success(self.request, "You have successfully logged in.")
            else:
                messages.error(self.request, "Check your login information.")
        return super(HomeView, self).form_invalid(form)


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


class LogoutView(generic_views.RedirectView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "You have successfully logged out.")
        return redirect('/')