
from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.password_validation import validate_password
# from rest_framework.fields import ImageField


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'profile_picture') #'rating', 'feedback_text'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)
    # default_error_messages = {
    #     'Email': 'This Email is already exists'}

    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','email', 'password']
        read_only_fields = ('updated_at','date_created', 'client_ip')

    # def create(self, validated_data):
    #     validated_data['user'] = self.context.get('request').META.get("REMOTE_ADDR")
    #     return User.objects.create(**validated_data)

    # def validate(self, attrs):
    #     email = attrs.get('email', '')
    #     # username = attrs.get('username', '')

        # if not email.isalnum():
        #     raise serializers.ValidationError(
        #         self.default_error_messages)
        # return attrs

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})

    #     return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
    # def create(self, validated_data):
    #     validated_data['email'] = self.context.get('request').META.get("REMOTE_ADDR")
    #     return User.objects.create(**validated_data)
        


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['id','email', 'password', 'tokens']

    
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')

        return {
            'id' : user.id, 
            'email': user.email,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token') 


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(required=True)
    # profile_picture = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_picture')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'profile_picture': {'required': False}
        }

    # def validate_email(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(email=user.email).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})
    #     return value

    # def validate_username(self, value):
    #     user = self.context['request'].user
    #     if User.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})
    #     return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.profile_picture = validated_data['profile_picture']
        # instance.profile_picture = validated_data['profile_picture']
        # instance.username = validated_data['username']
        instance.save()

        return instance

"""
class userRatingFeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('rating', 'feedback_text')
"""
class AnonymousRatingFeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RatingFeedback
        fields = ('rating', 'feedback_text')


class GuestUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GuestUser
        fields = ('secret_key','first_name', 'last_name', 'email', 'portfolio_name', 'amount', 'charities')

class TransactionSuccessfulSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuestUser
        fields = ('secret_key', 'transaction_successful_ID')


class UserTxnSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField(source='email')

    class Meta:
        model = UserTransaction
        fields = ('referrence_number', 'portfolio_name', 'amount', 'charities', 'user_id')

class UserTxnSuccessfulSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTransaction
        fields = ('referrence_number', 'transaction_successful_ID')

#for only admin
class AdminViewGuestUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuestUser
        fields = ("__all__")

class AdminViewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("__all__")

class NoOfTransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTransaction
        fields = ("__all__")