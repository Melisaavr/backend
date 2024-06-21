from rest_framework import serializers
from .models import User, Slot, Booking
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'password')
        extra_kwargs = {'full_name': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            username=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'day', 'start_time', 'end_time', 'seats']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
