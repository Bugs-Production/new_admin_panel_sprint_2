from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, Genre, Person


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ["get"]

    def get_queryset(self):
        films_work = FilmWork.objects.annotate(
            genres=ArrayAgg("genres_for_films__name", distinct=True),
            actors=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role="actor"),
                distinct=True,
            ),
            directors=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role="director"),
                distinct=True,
            ),
            writers=ArrayAgg(
                "persons__full_name",
                filter=Q(personfilmwork__role="writer"),
                distinct=True,
            ),
        ).values(
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
            "genres",
            "actors",
            "directors",
            "writers",
        )
        return films_work

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = FilmWork
    http_method_names = ["get"]  # Список методов, которые реализует обработчик
    paginate_by = 50

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by,
        )
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }

        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        movie_uuid = self.kwargs.get("pk")

        context = queryset.get(id=movie_uuid)

        return context
