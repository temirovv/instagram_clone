from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView


from .serializers import SignUpSerializer
from .models import User


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permisson_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer
