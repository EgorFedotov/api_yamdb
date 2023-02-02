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
    genres = GenreSerializer(many=True)
    category = CategorySerializer(many=False)

    def validate_year(self, year) -> int:
        if 600 < year < 2100:
            return year
        raise serializers.ValidationError("year not valid value")

    class Meta:
        model = Title
        fields = '__all__'
