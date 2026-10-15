from rest_framework import serializers

from account.models import User
from book.models import Author, Book, Collection, Genre, Review, ReviewLike


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "avatar",
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["pk", "name", "description", "slug"]


class AuthorSerializer(serializers.ModelSerializer):
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
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "book",
            "subject",
            "text",
            "likes",
            "parent",
            "star",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "book",
            "likes",
            "parent",
            "status",
            "created_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "book",
            "subject",
            "text",
            "likes",
            "parent",
            "star",
            "status",
            "created_at",
            "liked_by_me",
        ]
        read_only_fields = [
            "id",
            "user",
            "book",
            "likes",
            "parent",
            "status",
            "created_at",
        ]

    def get_liked_by_me(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        cache = self.context.setdefault("_liked_ids", {})

        if obj.book_id not in cache:
            cache[obj.book_id] = set(
                ReviewLike.objects.filter(
                    user=request.user, review__book_id=obj.book_id
                ).values_list("review_id", flat=True)
            )

        return obj.pk in cache[obj.book_id]


class ReviewReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "book",
            "parent",
            "text",
            "likes",
            "star",
            "status",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "book",
            "parent",
            "likes",
            "star",
            "status",
            "created_at",
        ]


class AllBooksSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    star_avg = serializers.DecimalField(decimal_places=1, max_digits=2, read_only=True)

    reviews_count = serializers.IntegerField(read_only=True)
    rating_status = serializers.CharField(read_only=True)
    # pages_sum  = serializers.IntegerField(read_only=True)
    class Meta:
        model = Book
        fields = [
            # "pages_sum",
            "id",
            "rating_status",
            "reviews_count",
            "star_avg",
            "author",
            "slug",
            "title",
            "about",
            "summary",
            "cover",
            "pages",
            "genres",
            "star",
            "publisher",
            "published_date",
            "created_at",
        ]


class DetailBooksSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    rating_status = serializers.CharField(read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    star_avg = serializers.DecimalField(decimal_places=1, max_digits=2, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "rating_status",
            "reviews_count",
            "star_avg",
            "author",
            "slug",
            "title",
            "about",
            "summary",
            "cover",
            "pages",
            "genres",
            "star",
            "reviews",
            "publisher",
            "published_date",
            "created_at",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    books = AllBooksSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = [
            "pk",
            "user",
            "books",
            "title",
            "cover",
            "description",
            "is_public",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "books",
            "created_at",
        ]


# test
class RecentReviewSerializer(ReviewSerializer):
    book_title = serializers.CharField(source="book.title", read_only=True)
    book_slug = serializers.CharField(source="book.slug", read_only=True)

    class Meta(ReviewSerializer.Meta):
        fields = ReviewSerializer.Meta.fields + ["book_title", "book_slug"]
