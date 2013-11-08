# serializers.py archivo de serializadores para API RESTRUCTUREDTEXT_FILTER_SETTINGS
from rest_framework import serializers
from .models import Enlace, Categoria
from django.contrib.auth.models import User

class EnlaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Enlace
        fields = ('url','titulo','enlace','votos','categoria','usuario','timestamp',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        field = ('url','username', 'email',)

class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        field = ('url','titulo',)