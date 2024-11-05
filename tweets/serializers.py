import random
import threading

from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from tweets.models import UserModel, TweetModel


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(
        write_only=True,
        max_length=13,
        validators=[
            UniqueValidator(
                queryset=UserModel.objects.all(),
                message="This phone number is already in use."
            )
        ]
    )
    confirmation_code = serializers.CharField(read_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'confirmation_code', 'email', 'phone_number', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords must match')
        return attrs

    def validate_phone_number(self, phone_number: str):
        phone_number = phone_number.strip()
        if not phone_number.startswith('+998'):
            raise serializers.ValidationError('Phone number must start with +998')
        return phone_number

    def validate_email(self, email):
        email = email.strip()
        if '@' not in email or '.' not in email:
            raise serializers.ValidationError('Email must contain "@" and a domain.')
        return email

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password
        confirmation_code = random.randint(1111, 9999)  # Generate confirmation code
        validated_data['confirmation_code'] = confirmation_code  # Save the code in validated_data
        user = UserModel.objects.create_user(**validated_data)
        user.is_active = False  # Mark user as inactive until confirmed
        user.confirmation_code = confirmation_code  # Store the confirmation code
        user.save()

        # Send confirmation email
        send_mail(
            'Your confirmation code',
            f'Your confirmation code is {confirmation_code}',
            'hmavlonov79@gmail.com',
            [validated_data['email']],
            fail_silently=False,
        )

        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        confirmation_code = attrs.get('confirmation_code')

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError('User not found.')

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Invalid confirmation code.')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel.objects.all()
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)


class TweetSerializer(serializers.Serializer):
    class Meta:
        model = TweetModel.objects.all()
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        tweet = TweetModel.objects.create(**validated_data)
        tweet.save()
        return tweet