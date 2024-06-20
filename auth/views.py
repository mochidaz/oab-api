from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from auth.auth import IsAdmin
from users.models import User
from users.serializers import UserSerializer
from common.serializers import ResponseSerializer


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['username'] = user.username
        token['id'] = user.id
        return token


class JwtObtain(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data.get('username'))
        except User.DoesNotExist:
            raise NotFound('User does not exist!')

        if not user.status == True:
            raise ValidationError({
                'email': ['User is not active']
            })

        if not user.check_password(request.data.get('password')):
            raise ValidationError({
                'password': ['Password is incorrect']
            })

        response = super().post(request, *args, **kwargs)

        response.data['username'] = user.username
        response.data['id'] = user.id

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': response.data,
        })

        return Response(serializer.data)


class RefreshToken(TokenRefreshView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': response.data,
        })

        return Response(serializer.data)


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        self.perform_create(serializer)

        resp = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "User created successfully"
            },
        })

        return Response(resp.data)