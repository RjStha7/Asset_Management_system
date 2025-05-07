import email
from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator



#User registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    #For password conformation
    password = serializers.CharField(style={'input_type':'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True, required=True)
    phone_number = serializers.CharField(source='userprofile.Phone_number', write_only=True)
    address = serializers.CharField(source='userprofile.address', write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', "phone_number", "address")

    # validating password and conform password
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    # def create(self, validate_data):
    #     validate_data.pop('password2', None)
    #     return User.objects.create_user(**validate_data)
    def create(self, validated_data):
        user_profile_data = validated_data.pop('userprofile', {})
        validated_data.pop('password2', None)
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **user_profile_data)
        return user
    



#User login   
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password']


#User profile
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.Phone_number', read_only=True)
    address = serializers.CharField(source='userprofile.address', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','phone_number', 'address']


#User password change
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'password', 'password2']
        extra_kwargs = {
            'old_password': {'write_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is not correct."})
        
        if password != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return attrs
    
    def save(self, **kwargs):
        user = self.context.get('user')
        password = self.validated_data.get('password')
        user.set_password(password)  # Set the new password
        user.save()  # Save the user instance
        return user
    

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate_email(self, value):
        # email = value.get('email')
        if User.objects.filter(email=value).exists():
            user = User.objects.get(email = value)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('reset token', token)
            link =f'http://localhost:3000/api/user/reset/{uid}/{token}'
            print('password resert link', link)
            return value

        else:
            raise ValidationError('Not a register user')
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True, required=True)
    
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid UID or user does not exist.")
        
        # Debugging logs
        print(f"UID: {uid}, Decoded User ID: {user_id}")
        print(f"Token: {token}")
        print(f"User: {user}")
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Token is not valid or expired.")
        
        # Store the user in the validated data for use in the save method
        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.Phone_number', read_only=True)
    address = serializers.CharField(source='userprofile.address', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','phone_number', 'address']