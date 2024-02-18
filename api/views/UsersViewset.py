from rest_framework import generics, viewsets
from api.serializers import UserSerializer
from api.models import User
from rest_framework.response import Response

class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request):
        name = request.data['name']
        username = request.data['username']
        password = request.data['password']
        role = request.data['role']

        newUser = User.objects.create(
            name=name,
            username=username,
            role=role
        )

        newUser.set_password(password)
        newUser.save()
        serializer = UserSerializer(newUser)

        return Response({'success': True, 'new_user': serializer.data})