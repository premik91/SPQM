from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import serializers, urlresolvers, mail
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils import crypto

from django.views import generic as generic_views
import time
from SPQM.frontend import forms

from SPQM.frontend.models import Person, Information, ExtendedUser
from SPQM import testing, settings


PERSONS_TO_SEND = 4


class HomeView(generic_views.FormView):
    template_name = 'frontend/home.html'
    form_class = forms.RegisterUserForm
    success_url = urlresolvers.reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        # testing.fill_db()
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Did register form have errors
        form_invalid = False
        if 'form_invalid' in self.request.session:
            form_invalid = True
            del self.request.session['form_invalid']
        context.update({
            'persons': Person.objects.all()[:4],
            'form_invalid': form_invalid
        })
        return context

    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        if len(username) == 0:
            username = email
        password = form.cleaned_data['password']

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        # Send confirmation token
        extended_user = ExtendedUser(user=user, confirmation_token=crypto.get_random_string(20))
        extended_user.save()
        extended_user.send_confirmation_mail()

        user = authenticate(username=username, password=password)
        login(self.request, user)

        messages.success(self.request, 'You have successfully been registered. You will receive mail to confirm your email.')
        return super(HomeView, self).form_valid(form)

    def form_invalid(self, form):
        # Load and send PERSONS_TO_SEND more persons
        if self.request.is_ajax():
            number_of_persons = int(self.request.POST['number_of_persons'])
            json = serializers.serialize(
                'json',
                Person.objects.all()[number_of_persons:number_of_persons + PERSONS_TO_SEND],
                indent=4,
                relations=('information', )
            )
            time.sleep(1)
            return HttpResponse(json)
        # If email is not in POST, than this is login
        elif 'email' not in self.request.POST:
            username = self.request.POST['username']
            password = self.request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(self.request, user)
                messages.success(self.request, 'You have successfully logged in.')
            else:
                messages.error(self.request, 'Check your login information.')
        # Else register form is wrong
        else:
            self.request.session['form_invalid'] = True

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
        messages.success(self.request, 'You have successfully logged out.')
        return redirect('/')


class EmailConfirmationView(generic_views.RedirectView):
    def get(self, request, *args, **kwargs):
        try:
            token = kwargs.get('confirmation_token')
            user = ExtendedUser.objects.get(confirmation_token=token)
            if user.check_token(token):
                user.email_confirmed = True
                user.save()
                messages.success(request, 'You have successfully confirmed your e-mail address.')
            else:
                messages.error(request, 'Invalid confirmation token.')
            return redirect('/')
        except (ValueError, ObjectDoesNotExist):
            raise Http404


class ContactView(generic_views.FormView):
    template_name = 'frontend/contact.html'
    form_class = forms.ContactForm
    success_url = urlresolvers.reverse_lazy('contact')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject'] + ': ' + first_name + ' ' + last_name
        message = form.cleaned_data['message']

         # After debugging, delete "'i@premik91.com'"
        mail.send_mail(subject, message, settings.ADMINS[0][1], [email, 'i@premik91.com'])
        messages.success(self.request, 'You have successfully sent an email.')
        return super(ContactView, self).form_valid(form)


class AddPersonView(generic_views.FormView):
    template_name = 'frontend/add_person.html'
    form_class = forms.AddPersonForm
    success_url = urlresolvers.reverse_lazy('add_person')

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']

        # messages.success(self.request, 'You have successfully added a person.')
        return super(AddPersonView, self).form_valid(form)
