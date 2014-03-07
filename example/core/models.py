from localflavor.us.models import USStateField
from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=200)
    fruit_image = models.ImageField(upload_to="fruitimages")
    desc = models.TextField("description")

    def __unicode__(self):
        return self.name


class Farm(models.Model):
    name  = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='farms')
    fruit = models.ManyToManyField(Fruit)

    def __unicode__(self):
        return u"{0}'s Farm: {1}".format(self.owner.username, self.name)


class City(models.Model):
    name = models.CharField(max_length=200)
    state = USStateField()

    def __unicode__(self):
        return self.name


class ReferencesTest(models.Model):
    city   = models.ForeignKey(City)
    fruit  = models.ForeignKey(Fruit, related_name="first_r")
    fruit2 = models.ForeignKey(Fruit, related_name="second_r")
    farm   = models.ForeignKey(Farm, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('example-detail', [str(self.id)])

    def __unicode__(self):
        ret = u"{0}: {1} - {2} - {3}".format(str(self.pk), self.city, self.fruit, self.fruit2)
        if self.farm:
            ret += u" - {0}".format(self.farm)
        return ret
