from django.db import models
from django.core.validators import RegexValidator

class Country(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"

    def __str__(self):
        return self.name


class AnimalClass(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "AnimalClass"
        verbose_name_plural = "AnimalClasses"

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.name


class Fodder(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Fodder"
        verbose_name_plural = "Fodders"

    def __str__(self):
        return self.name


class Placement(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=30)
    basin = models.BooleanField()
    area = models.FloatField()

    class Meta:
        ordering = ['name', 'number']
        verbose_name = "Placement"
        verbose_name_plural = "Placements"

    def __str__(self):
        return f'{self.name} {self.number}'

class Staffer(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="Phone number must be in the format: '+375 (29) XXX-XX-XX'"
    )

    name = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20, validators=[phone_regex], default='+375 (29) XXX-XX-XX')
    username = models.CharField(max_length=30, default='')

    class Meta:
        verbose_name = "Staffer"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f'{self.post} {self.name}'


class Animal(models.Model):
    name = models.CharField(max_length=30)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True, blank=True)
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.SET_NULL, null=True, blank=True)
    staffer = models.ForeignKey(Staffer, on_delete=models.SET_NULL, null=True, blank=True, related_name='animals')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    placement = models.ForeignKey(Placement, on_delete=models.SET_NULL, null=True, blank=True, related_name='animals')
    fodder = models.ForeignKey(Fodder, on_delete=models.SET_NULL, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.URLField(default='')
    info = models.TextField(default='')
    daily_feed = models.FloatField(default=0)

    class Meta:
        ordering = ["admission_date"]
        verbose_name = "Animal"
        verbose_name_plural = "Animals"

    def __str__(self):
        return f'{self.species} {self.name}'
