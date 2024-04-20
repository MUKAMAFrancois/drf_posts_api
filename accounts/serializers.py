from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password




class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text='Enter your email',
        label='Email',
        error_messages={'required': 'Email is required'}
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text='Enter your username',
        label='Username',
        error_messages={'required': 'Username is required'}
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text='Enter your password',
        label='Password',
        error_messages={'required': 'Password is required'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Repeat your password',
        label='Repeat Password',
        error_messages={'required': 'Please repeat your password'}
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2', 'first_name', 'last_name', 'bio', 'photo', 'is_active', 'is_staff', 'date_joined')
        extra_kwargs = {
            'first_name': {'required': False, 'help_text': 'Enter your first name', 'label': 'First Name'},
            'last_name': {'required': False, 'help_text': 'Enter your last name', 'label': 'Last Name'},
            'bio': {'required': False, 'help_text': 'Enter your bio', 'label': 'Bio'},
            'photo': {'required': False, 'help_text': 'Upload your photo', 'label': 'Photo'}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            photo=validated_data.get('photo', ''),
            is_active=validated_data.get('is_active', True),
            is_staff=validated_data.get('is_staff', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
