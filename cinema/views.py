from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from cinema.models import (
    Order,
    Movie,
    MovieSession,
    Genre,
    Actor,
    CinemaHall,
)
from cinema.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSessionListSerializer,
    MovieSessionDetailSerializer,
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer,
)
from cinema.filters import MovieFilterSet, MovieSessionFilterSet


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by("id")
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all().order_by("id")
    serializer_class = ActorSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all().order_by("id")
    serializer_class = CinemaHallSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "tickets__movie_session"
        ).order_by("id")


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilterSet
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieListSerializer


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.select_related(
        "movie", "cinema_hall"
    ).order_by("id")
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieSessionFilterSet
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionListSerializer
