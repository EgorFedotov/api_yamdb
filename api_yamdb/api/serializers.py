from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(required=False, many=True)
    category = CategorySerializer(required=False, many=False)

    def validate_year(self, value):
        if 1600 < value < 2100:
            return value
        raise serializers.ValidationError("Year is not valid value")

    class Meta:
        model = Title
        fields = '__all__'
