import factory  
import factory.django

class UserFactory(factory.django.DjangoModelFactory):  
    class Meta:
        model = User

    