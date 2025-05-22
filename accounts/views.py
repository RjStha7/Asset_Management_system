from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from accounts.serializers import ChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from accounts.renderer import UserRenderer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from asset.pagination import CustomPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# Create your views here.

#Generate token mannualy
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


#user registration
class UserRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    renderer_classes = [UserRenderer]
    def post(self, request, format =None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#user login  
# class UserLoginView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self, request, format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.validated_data.get('email')
#             password = serializer.validated_data.get('password')
#             user = authenticate(email=email, password=password)
            
#             if user is not None:
#                 token = get_tokens_for_user(user)
#                 return Response({
#                     'token': token,
#                     'is_admin': user.is_staff,
#                     'message': 'Login successful'
#                     }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

# with this code cookes is set automatically
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            response = Response({
                'token': token,
                'is_admin': user.is_staff,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
            # Set access token as HTTP-only, Secure cookie
            response.set_cookie(
                key='access_token',
                value=token['access'],
                httponly=False,
                secure=False,  # Only sent over HTTPS
                # samesite='Lax',  # Or 'Strict' for more security
                max_age=60*60  # 1 hour, adjust as needed
            )
            # Optionally set refresh token as cookie too
            response.set_cookie(
                key='refresh_token',
                value=token['refresh'],
                httponly=False,
                secure=False,
                # samesite='Lax',
                max_age=7*24*60*60  # 7 days, adjust as needed
            )
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                

#user logout
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        try:
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
class UserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        try:
            users = User.objects.all()
            paginator = CustomPagination()
            paginated_users = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(paginated_users, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Error fetching users', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    renderer_classes = [UserRenderer]
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Save the new password
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # email = serializer.validated_data.get('email')
            
            return Response({'message': 'Password reset email sent successfully. Please check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')    
class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    endpoints = {
        'Register': '/api/user/register/',
        'Login': '/api/user/login/',
        'Logout': '/api/user/logout/',
        'All_Users': '/api/user/users/',
        'Change Password': '/api/user/change-password/',
        'Send Reset Password Email': '/api/user/send-reset-password-email/',
        'Reset Password': '/api/user/reset-password/<uid>/<token>/',
        'User Profile': '/api/user/user-profile/',
        'Admin Verify': '/api/user/admin-verify/',
        "Categories": "/api/categories/",
        "Assets": "/api/assets/",
        "Asset-details": "/api/asset-details/",
        "Asset-out": "/api/asset-out/"

    }
    return Response(endpoints)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_verify(request):
    user = request.user
    return Response({
        'is_admin': user.is_staff,
        'is_superuser': user.is_superuser,
    })   

