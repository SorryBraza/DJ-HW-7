from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Advertisement
from .serializers import AdvertisementSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import AdvertisementFilter


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "delete"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []
