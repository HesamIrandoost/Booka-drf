from django.db import models
from django.db.models import F, Value, Q, Count, Avg, Sum, Min, Max, Case, When, CharField


class BookQuerySet(models.QuerySet):

    def rate(self):
        return self.annotate(
            rating_status=Case(
                        When(star__gte=4, then=Value("Excellent")),
                        When(star__gte=3, then=Value("Good")),
                        default=Value("Bad"),
                        output_field=CharField()),)

    def with_author(self):
        return self.select_related("author")

    def filter_genre(self, genre):
        return self.filter(genres__slug__in=genre).annotate(
                    matched_genre=Count(
                        "genres", filter=Q(genres__slug__in=genre), distinct=True),
                ).filter(matched_genre=len(genre))