import re
from django.db import models
from django.utils import timezone
from django.utils.translation import to_locale, get_language
from cities_light import models as cities_models


class Information(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

    city = models.ForeignKey(cities_models.City)
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
    date_added = models.DateTimeField(default=timezone.now())

    category = models.ForeignKey(Category)
    description = models.CharField(max_length=10000)

    def __unicode__(self):
        return unicode(self.information.first_name)

    def create_url(self):
        proper_url = re.sub(r"[^a-zA-Z0-9 ]", '', self.name)
        proper_url = proper_url.replace(' ', '_')
        proper_url = proper_url + '-' + self.pk.__str__()
        return proper_url