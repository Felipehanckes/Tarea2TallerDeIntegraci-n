from rest_framework import serializers
from . models import Burguer, Ingredient

class BurguerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Burguer
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'