from rest_framework import serializers

from reviews.models import Category, Genre, Title, User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    def validate_year(self, year) -> int:
        if 600 < year < 2100:
            return year
        raise serializers.ValidationError("year not valid value")

    class Meta:
        model = Title
        fields = '__all__'


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
