from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import RegistrationSerializer
from django.contrib.auth import authenticate

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.permissions import IsAuthenticated
from auth_app.models import User
from .serializers import UserSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)

            return Response({
                'token': token.key,
                'fullname': user.fullname,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_200_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(
            username=email,
            password=password
        )

        if user is None:
            return Response(
                {'error': 'E-Mail oder Passwort ist falsch.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'fullname': user.fullname,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_200_OK)


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response(
                {'detail': 'E-Mail-Adresse fehlt.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {'detail': 'Ungültige E-Mail-Adresse.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'E-Mail-Adresse nicht gefunden.'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )