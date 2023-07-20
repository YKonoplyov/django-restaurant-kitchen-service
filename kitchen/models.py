from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=255)


class DishType(models.Model):
    type = models.CharField(max_length=255)


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="cooks")
    years_of_experience = models.IntegerField()

    def get_absolute_url(self):
        return reverse("kitchen:cook-list")


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")
    cooks = models.ManyToManyField(Cook, related_name="dishes")

