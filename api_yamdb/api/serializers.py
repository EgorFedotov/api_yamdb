from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)

    class Meta:
        fields = '__all__'
        model = User


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Username "me" is not valid')
        return value

    class Meta:
        fields = '__all__'
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
