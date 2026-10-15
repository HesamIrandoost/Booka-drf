# alternate_serializers.py

from rest_framework import serializers
from .serializers import AllBooksSerializer
from book.models import Author, Book, Collection, Genre, Review


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = AllBooksSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            "pk",
            "slug",
            "first_name",
            "last_name",
            "profile",
            "biography",
            "website",
            "date_born",
            "place_born",
            "books",
        ]


class GenreDetailSerializer(serializers.ModelSerializer):
    books = AllBooksSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = [
            "pk",
            "name",
            "description",
            "books",
        ]
