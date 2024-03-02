from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию
        if self.context['request'].method == 'POST':
            if Advertisement.objects.filter(creator_id=self.context['request'].user, status='OPEN').count() > 9:
                raise serializers.ValidationError('Открытых объявлений может быть не больше 10')
            else:
                return data
        if self.context['request'].method == 'PATCH' and self.context['request'].data['status'] == 'OPEN':
            if Advertisement.objects.filter(creator_id=self.context['request'].user, status='OPEN').count() > 9:
                raise serializers.ValidationError('Открытых объявлений может быть не больше 10')
            else:
                return data
        return data
