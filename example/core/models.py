from django.contrib.localflavor.us.models import USStateField
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
        return u"%s's Farm: %s" % (self.owner.username, self.name)


class City(models.Model):
    name = models.CharField(max_length=200)
    state = USStateField()

    def __unicode__(self):
        return self.name


class ReferencesTest(models.Model):
    city   = models.ForeignKey(City)
    fruit  = models.ForeignKey(Fruit, related_name="first_r")
    fruit2 = models.ForeignKey(Fruit, related_name="second_r")
    farm   = models.ForeignKey(Farm)
