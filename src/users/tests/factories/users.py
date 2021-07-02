import factory


class UnikubeUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.UnikubeUser"
