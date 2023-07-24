from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kitchen:dish-type-list")


class Position(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CookManager(BaseUserManager):
    def create_superuser(self,
                         username,
                         years_of_experience,
                         password,):
        user = self.model(
            username=username,
            position_id = Position.objects.get(id=1).id,
            years_of_experience=years_of_experience
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Cook(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="cooks"
    )
    years_of_experience = models.IntegerField()

    custom_objects = CookManager()

    def get_absolute_url(self):
        return reverse("kitchen:cook-detail", kwargs={"pk": self.pk})

    REQUIRED_FIELDS = ["years_of_experience"]


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name="dishes")
    cooks = models.ManyToManyField(Cook, related_name="dishes")
    finished_cooks = models.ManyToManyField(
        Cook,
        related_name="dishes_finished",
        blank=True
    )

    def progres_percent(self):
        return round(
            len(self.finished_cooks.all()) / len(self.cooks.all()), 2
        ) * 100

    def get_absolute_url(self):
        return reverse("kitchen:dish-list")

    def __str__(self):
        return self.name
