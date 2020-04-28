
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Burguer.models import Burguer, Ingredient
from Burguer.serializer import BurguerSerializer, IngredientSerializer

# Create your views here.

class BurguerList(APIView):
    def get(self, request):
        burguers = Burguer.objects.all()
        serializer = BurguerSerializer(burguers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request2 = request.data.copy()
        ingredientes = request2.__getitem__('ingredientes').replace(' ','')
        ingredientes = ingredientes.split(',')
        ingredientes = [int(x) for x in ingredientes if x != '']
        request2.setlist('ingredientes', ingredientes)
        serializer = BurguerSerializer(data=request2)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BurguerDetail(APIView):
    def get_object(self, pk):
        try:
            return Burguer.objects.get(pk=pk)
        except Burguer.DoesNotExist:
            raise Http404   

    def get(self, request, pk, format=None):
        burguer = self.get_object(pk)
        serializer = BurguerSerializer(burguer)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        burguer = self.get_object(pk)
        try:
            if request.data["ingredientes"] != None:
                return Response("No es posible cambiar los Ingredientes de una " +
                "hamburguesa desde aqui :(", status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        try:
            if request.data["id"] != None:
                return Response("No es posible cambiar el ID de una hamburguesa" +
                "desde aqui :(", status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        serializer = BurguerSerializer(burguer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Se realizó el cambio esperado :)", status= status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        burguer = self.get_object(pk)
        burguer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IngredientList(APIView):

    def get(self, request):
        ingredient_all = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredient_all, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IngredientDetail(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404   

    def get(self, request, pk, format=None):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        print('Si entro')
        try:
            Burguer.objects.filter(ingredientes=pk)[0]
            return Response("No se puede eliminar el Ingrediente, ya que " + 
            "es el ingrediente de una hamburguesa", status=status.HTTP_400_BAD_REQUEST)
        except:
            print("no se encontro ingrediente en las burgas")
            ingredient = self.get_object(pk)
            ingredient.delete()
            return Response("Se ha eliminado el Ingrediente ya que no " + 
            "pertenecía a ninguna hamburguesa.", status=status.HTTP_200_OK)

class BurguerIngredient(APIView):
    def get_burguer(self, pk):
        try:
            return Burguer.objects.get(pk=pk)
        except Burguer.DoesNotExist:
            return 0 
    
    def get_ingredient(self,pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            return 0

    def put(self, request, pk1, pk2, format= None):
        burguer = self.get_burguer(pk1)
        ingredient = self.get_ingredient(pk2)
        if ingredient == 0:
            return Response('No Existe ese ingrediente', status=status.HTTP_404_NOT_FOUND)
        elif burguer == 0:
            return Response('No Existe esa hamburguesa', status=status.HTTP_404_NOT_FOUND)
        else:
            burguer.ingredientes.add(ingredient)
            return Response("se ha agregado", status=status.HTTP_200_OK)
    
    def delete(self, request, pk1, pk2, format=None):
        burguer = self.get_burguer(pk1)
        ingredient = self.get_ingredient(pk2)
        if ingredient == 0:
            return Response('No Existe ese ingrediente', status=status.HTTP_404_NOT_FOUND)
        elif burguer == 0:
            return Response('No Existe esa hamburguesa', status=status.HTTP_404_NOT_FOUND)
        else:
            burguer.ingredientes.remove(ingredient)
            return Response("se ha removido exitosamente", status=status.HTTP_200_OK)
