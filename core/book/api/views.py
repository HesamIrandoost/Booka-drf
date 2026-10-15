# views.py
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F, Value, Q, Count, Avg, Sum, Min, Max, Case, When, CharField
from django.db.models.functions import Greatest

from book.models import Author, Book, Collection, Genre, Review, ReviewLike
from book.tasks import send_review_notification
from .querysets import BookQuerySet

from .filters import BookFilter
from .pagination import BookPagination
from .serializers import (
    AllBooksSerializer,
    AuthorSerializer,
    CollectionSerializer,
    DetailBooksSerializer,
    GenreSerializer,
    ReviewSerializer,
    ReviewReplySerializer,
)
from .alternate_serializers import AuthorDetailSerializer, GenreDetailSerializer

# =========================================================
# Books
# =========================================================


class AllBookListView(generics.ListAPIView):
    serializer_class = AllBooksSerializer
    pagination_class = BookPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ["title", "author__first_name", "author__last_name", "genres__name"]
    filterset_class = BookFilter
    ordering_fields = [
        "title",
        "author",
        "star",
        "published_date",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Book.objects.with_author().prefetch_related("genres")

        min_rating = self.request.query_params.get("min_rating")
        max_rating = self.request.query_params.get("max_rating")
        min_pub_date = self.request.query_params.get("min_pub_date")
        max_pub_date = self.request.query_params.get("max_pub_date")
        genres = self.request.query_params.get("genre")
        filters = Q()

        if min_rating:
            filters &= Q(star__gte=min_rating)
        if max_rating:
            filters &= Q(star__lte=max_rating)
        if min_pub_date:
            filters &= Q(published_date__gte=min_pub_date + "-1-1")
        if max_pub_date:
            filters &= Q(published_date__lte=max_pub_date + "-1-1")

        if genres:
            genre = genres.split(",")
            q_genre = (
                queryset.filter_genre(genre)
            )
            queryset = q_genre

        return queryset.filter(filters).annotate(
            star_avg=Avg("reviews__star"), 
            reviews_count=Count("reviews", distinct=True),
            ).rate()



class DetailBookView(generics.RetrieveAPIView):
    serializer_class = DetailBooksSerializer
    lookup_field = "slug"

    queryset = (
        Book.objects.annotate(
            reviews_count=Count("reviews"), star_avg=Avg("reviews__star"),
        ).rate()
        .with_author()
        .prefetch_related(
            "genres",
            "reviews__user",
        )
        .all()
    )


# =========================================================
# Reviews
# =========================================================


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return (
            Review.objects.filter(
                book__slug=self.kwargs["slug"],
                status=True,
            )
            .select_related("user", "book")
            .prefetch_related("replies__user")
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, slug=self.kwargs["slug"])
        star = serializer.validated_data.get("star", 0)

        if not 1 <= star <= 5:
            raise ValidationError({"star": ["Choose a rating from 1 to 5."]})

        if Review.objects.filter(
            user=self.request.user, book=book, parent__isnull=True
        ).exists():
            raise ValidationError({"detail": "You have already reviewed this book."})

        review = serializer.save(user=self.request.user, book=book)

        send_review_notification.delay(
            self.request.user.id,
            review.book.title,
        )

        book.update_star()


class ReviewReplyCreateView(generics.CreateAPIView):
    serializer_class = ReviewReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs["pk"], status=True)
        parent = review.parent or review

        serializer.save(
            user=self.request.user,
            book=parent.book,
            parent=parent,
            subject="Reply",
        )


class ReviewLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk, status=True)

        if review.user_id == request.user.id:
            raise ValidationError({"detail": "You can't like your own review."})

        with transaction.atomic():
            like, created = ReviewLike.objects.get_or_create(
                user=request.user, review=review
            )

            if created:
                Review.objects.filter(pk=review.pk).update(likes=F("likes") + 1)
            else:
                like.delete()
                Review.objects.filter(pk=review.pk).update(
                    likes=Greatest(F("likes") - 1, Value(0))
                )

        review.refresh_from_db(fields=["likes"])

        return Response({"liked": created, "likes": review.likes})


# =========================================================
# Authors
# =========================================================


class AuthorListView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    pagination_class = BookPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ["first_name", "last_name"]
    filterset_fields = {"slug": ["iexact"]}
    ordering_fields = [
        "slug",
    ]

    queryset = Author.objects.all()


class AuthorDetailView(generics.RetrieveAPIView):
    serializer_class = AuthorDetailSerializer
    lookup_field = "slug"
    filter_backends = [
        SearchFilter,
    ]

    search_fields = ["books__title"]
    queryset = Author.objects.prefetch_related("books").all()


# =========================================================
# Genres
# =========================================================


class GenreListView(generics.ListAPIView):
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]

    search_fields = ["name"]
    filterset_fields = {"slug": ["iexact"]}
    ordering_fields = [
        "slug",
    ]

    queryset = Genre.objects.all()


class GenreDetailView(generics.RetrieveAPIView):
    serializer_class = GenreDetailSerializer
    # lookup_field = "pk"
    lookup_field = "slug"
    filter_backends = [
        SearchFilter,
    ]

    search_fields = [
        "books__title",
        "author__first_name",
        "author__last_name",
    ]
    queryset = Genre.objects.prefetch_related("books").all()


# =========================================================
# Collections
# =========================================================


class CollectionListView(generics.ListCreateAPIView):
    serializer_class = CollectionSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = [
        "books__title",
        "books__author__first_name",
        "books__author__last_name",
        "user__username",
    ]
    ordering_fields = ["title", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Collection.objects.filter(is_public=True)
            .select_related("user")
            .prefetch_related(
                "books__author",
                "books__genres",
            )
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionUserListView(generics.ListCreateAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]

    search_fields = [
        "books__title",
        "books__author__first_name",
        "books__author__last_name",
    ]
    ordering_fields = ["slug", "title", "created_at"]
    filterset_fields = ["is_public"]

    def get_queryset(self):
        return (
            Collection.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related(
                "books__author",
                "books__genres",
            )
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        SearchFilter,
    ]

    search_fields = [
        "books__title",
        "books__author__first_name",
        "books__author__last_name",
    ]

    # lookup_field = 'pk'
    def get_queryset(self):
        return (
            Collection.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related(
                "books__author",
                "books__genres",
            )
        )


class CollectionPublicDetailView(generics.RetrieveAPIView):
    """for all users"""

    serializer_class = CollectionSerializer
    filter_backends = [
        SearchFilter,
    ]

    search_fields = [
        "books__title",
        "books__author__first_name",
        "books__author__last_name",
    ]

    # lookup_field = 'pk'
    def get_queryset(self):
        return (
            Collection.objects.filter(is_public=True)
            .select_related("user")
            .prefetch_related(
                "books__author",
                "books__genres",
            )
        )


class AddBookToCollectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, book_id):
        collection = get_object_or_404(
            Collection,
            pk=pk,
            user=request.user,
        )

        book = get_object_or_404(
            Book,
            pk=book_id,
        )

        collection.books.add(book)
        return Response({"detail": "Book added to collection."})


class RemoveBookFromCollectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, book_id):
        collection = get_object_or_404(
            Collection,
            pk=pk,
            user=request.user,
        )

        book = get_object_or_404(
            Book,
            pk=book_id,
        )

        collection.books.remove(book)
        return Response({"detail": "Book removed from collection."})


# test
from .serializers import RecentReviewSerializer


class RecentReviewListView(generics.ListAPIView):
    serializer_class = RecentReviewSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        return (
            Review.objects.filter(status=True, parent__isnull=True)
            .select_related("user", "book")
            .order_by("-created_at")[:6]
        )
