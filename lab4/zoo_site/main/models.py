from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class AnimalClass(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Fodder(models.Model):
    name = models.CharField(max_length=30)
    # price = models.FloatField()

    def __str__(self):
        return self.name


class Placement(models.Model):
    number = models.IntegerField()
    name = models.CharField()
    basin = models.BooleanField()
    area = models.FloatField()
    # animals

    def __str__(self):
        pass


class Staffer(models.Model):
    name = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    # animals =

    def __str__(self):
        pass


class Animal(models.Model):
    name = models.CharField(max_length=30)
    species = models.ForeignKey(Species, on_delete=models.SET_NULL, null=True)
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.SET_NULL, null=True)
    staffer = models.ForeignKey(Staffer, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    placement = models.ForeignKey(Placement, on_delete=models.SET_NULL, null=True)
    fodder = models.ForeignKey(Fodder, on_delete=models.SET_NULL, null=True)
    admission_date = models.DateField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField()
    info = models.TextField()
    daily_feed = models.FloatField()

    class Meta:
        ordering = ["admission_date"]

    def __str__(self):
        return f'{self.species} {self.name}'
