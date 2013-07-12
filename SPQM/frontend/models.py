import re
from django.contrib.auth.models import User
from django.core import mail
from django.db import models
from django.template import loader
from django.utils import timezone
from django.utils.translation import to_locale, get_language
from cities_light import models as cities_models
from SPQM import settings


class Information(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    city = models.CharField(max_length=50)  # models.ForeignKey(cities_models.City)
    street = models.CharField(max_length=50)


class Category(models.Model):
    en_name = models.CharField(max_length=50)
    sl_name = models.CharField(max_length=50)

    description = models.CharField(max_length=10000)

    def __unicode__(self):
        if to_locale(get_language()) == 'sl':
            return unicode(self.sl_name)
        else:
            return unicode(self.en_name)


class Person(models.Model):
    information = models.ForeignKey(Information)
    active = models.BooleanField(default=True)
    validated = models.BooleanField(default=False)
    fictional = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now())

    category = models.ForeignKey(Category)
    description = models.CharField(max_length=10000)

    def __unicode__(self):
        return unicode(self.information.first_name + ' ' + self.information.last_name)

    def create_url(self):
        proper_url = re.sub(r"[^a-zA-Z0-9 ]", '', self.information.first_name + ' ' + self.information.last_name)
        proper_url = proper_url.replace(' ', '_')
        # Is the name unique?
        if not len(Information.objects.filter(first_name=self.information.first_name, last_name=self.information.last_name)) == 1:
            proper_url = proper_url + '-' + self.id.__str__()
        return '/' + proper_url + '/'


CONFIRMATION_TOKEN_VALIDITY = 5  # Days


class ExtendedUser(models.Model):
    user = models.ForeignKey(User)

    confirmation_token = models.CharField(max_length=50)
    confirmation_token_created_time = models.DateTimeField(default=timezone.now())
    email_confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.user.username)

    def check_token(self, confirmation_token):
        if confirmation_token != self.confirmation_token:
            return False
        elif (timezone.now() - self.confirmation_token_created_time).days > CONFIRMATION_TOKEN_VALIDITY:
            return False
        else:
            return True

    def send_confirmation_mail(self):
        context = {
            'EMAIL_SUBJECT_PREFIX': settings.EMAIL_SUBJECT_PREFIX,
            'SITE_NAME': settings.SITE_NAME,
            'SITE_URL': settings.SITE_URL,
            'CONFIRMATION_TOKEN_VALIDITY': CONFIRMATION_TOKEN_VALIDITY,
            'confirmation_token': self.confirmation_token,
            'user': self.user,
        }
        subject = loader.render_to_string('emails/confirmation_email_subject.txt', context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = loader.render_to_string('emails/confirmation_email.txt', context)
        # After debugging, delete "'i@premik91.com'
        mail.send_mail(subject, message, settings.ADMINS[0][1], [self.user.email, 'i@premik91.com'])