from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import UserCreateSerializer, UserSerializer


class UserApiViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
