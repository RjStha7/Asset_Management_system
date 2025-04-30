from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

#User registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    #For password conformation
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    # validating password and conform password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validate_data):
        validate_data.pop('password2', None)
        return User.objects.create_user(**validate_data)
    



#User login   
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password']


#User profile
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


#User password change
# class ChangePasswordSerializer(serializers.ModelSerializer):
#     old_password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)
#     password= serializers.CharField(max_length=128), style={'input_type': 'password'}, write_only=True, validators=[validate_password]
#     password2 = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True, required=True)

#     class Meta:
#         model=User
#         fields = ['old_password', 'password', 'password2']
#         extra_kwargs = {
#             'old_password': {'write_only': True},
#             'password': {'write_only': True}
#         }

#     def validate(self, attrs):
#         user = self.context.get('user')
#         old_pass
