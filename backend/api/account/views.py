from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from . import serializers as account_serializers



class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = account_serializers.RegisterSerializer(data = data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': f"User {user.username} created successfully .",
                            "data": serializer.data, }, status=status.HTTP_201_CREATED)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self, request):
        data = request.data
        # serializer = account_serializers.LoginSerializer(data = data)
        # if serializer.is_valid():
        username = data.get("username")
        password = data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)            
            return Response({"refresh_token": str(refresh),
                             "access_token": str(refresh.access_token),
                            })
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


# class ProfileView(APIView):
#     permission_classess = [IsAuthenticated]
#     def get(self, request):
#         user = request.user
#         serializer = account_serializers.RegisterSerializer(user)
#         return Response(serializer.data)