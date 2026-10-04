import django_filters
from book.models import Book


class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name="author__slug",
        lookup_expr="iexact",
    )

    class Meta:
        model = Book
        fields = [
            "author",
            "publisher",
        ]


# import django_filters
# from django.db.models import Count, Q

# from book.models import Book


# class BookFilter(django_filters.FilterSet):

#     author = django_filters.CharFilter(
#         field_name="author__slug",
#         lookup_expr="iexact",
#     )

#     min_rating = django_filters.NumberFilter(
#         field_name="star",
#         lookup_expr="gte",
#     )

#     max_rating = django_filters.NumberFilter(
#         field_name="star",
#         lookup_expr="lte",
#     )

#     min_pub_date = django_filters.NumberFilter(
#         method="filter_min_pub_date",
#     )

#     max_pub_date = django_filters.NumberFilter(
#         method="filter_max_pub_date",
#     )

#     genre = django_filters.CharFilter(
#         method="filter_genres",
#     )

#     def filter_min_pub_date(self, queryset, name, value):
#         return queryset.filter(
#             published_date__gte=f"{value}-01-01"
#         )

#     def filter_max_pub_date(self, queryset, name, value):
#         return queryset.filter(
#             published_date__lte=f"{value}-01-01"
#         )

#     def filter_genres(self, queryset, name, value):
#         genres = value.split(",")

#         return (
#             queryset
#             .filter(genres__slug__in=genres)
#             .annotate(
#                 matched_genre=Count(
#                     "genres",
#                     filter=Q(genres__slug__in=genres),
#                     distinct=True,
#                 )
#             )
#             .filter(matched_genre=len(genres))
#         )

#     class Meta:
#         model = Book
#         fields = [
#             "author",
#             "publisher",
#             "min_rating",
#             "max_rating",
#             "min_pub_date",
#             "max_pub_date",
#             "genre",
#         ]
