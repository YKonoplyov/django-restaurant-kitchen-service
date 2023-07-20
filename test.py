from django.contrib.auth import get_user_model
from kitchen.models import Position
get_user_model().objects.create_user(
    username="helper.cook",
    email="helper_cook@kitchen.com",
    password="Admin654",
    first_name="mykola",
    last_name="poroshenko",
    position=Position.objects.get(id=2),
    years_of_experience=2
)

