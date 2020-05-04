
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request2 = request.data.copy()
        try:
            ingredientes = request2.__getitem__('ingredientes').replace(' ','')
            ingredientes = ingredientes.split(',')
            ingredientes = [int(x) for x in ingredientes if x != '']
            request2.setlist('ingredientes', ingredientes)
        except:
            pass
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
            return 0   

    def get(self, request, pk, format=None):
        try:
            pk = int(pk)
        except:
            return Response('id invalido', status=status.HTTP_400_BAD_REQUEST)
        burguer = self.get_object(pk)
        if burguer == 0:
            return Response('Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)
        serializer = BurguerSerializer(burguer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        try:
            pk = int(pk)
        except:
            return Response('id invalido', status=status.HTTP_400_BAD_REQUEST)
        burguer = self.get_object(pk)
        if burguer == 0:
            return Response('Hambuerguesa Inexistente', status=status.HTTP_404_NOT_FOUND)
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

    def delete(self, request, pk, format=None):
        try:
            pk = int(pk)
        except:
            return Response('id invalido', status=status.HTTP_400_BAD_REQUEST)
        burguer = self.get_object(pk)
        if burguer == 0:
            return Response('Hamburguesa inexistente', status=status.HTTP_404_NOT_FOUND)
        burguer.delete()
        return Response('Hamburguesa Eliminada con existo', status=status.HTTP_200_OK)

class IngredientList(APIView):

    def get(self, request):
        ingredient_all = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredient_all, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return 0   

    def get(self, request, pk, format=None):
        try:
            pk = int(pk)
        except:
            return Response('id invalido', status=status.HTTP_400_BAD_REQUEST)
        ingredient = self.get_object(pk)
        if ingredient == 0:
            return Response('Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        try:
            pk = int(pk)
        except:
            return Response('id invalido', status=status.HTTP_400_BAD_REQUEST)
        try:
            Burguer.objects.filter(ingredientes=pk)[0]
            return Response("No se puede eliminar el Ingrediente, ya que " + 
            "es el ingrediente de una hamburguesa", status=status.HTTP_409_CONFLICT)
        except:
            print("no se encontro ingrediente en las burgas")
        ingredient = self.get_object(pk)
        if ingredient == 0:
            return Response('Ingrediente inexistente', status=status.HTTP_404_NOT_FOUND)
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
        try:
            pk1 = int(pk1)
        except:
            return Response('id hamburguesa invalido', status=status.HTTP_400_BAD_REQUEST)
        try:
            pk2 = int(pk2)
        except:
            return Response('id ingrediente invalido', status=status.HTTP_400_BAD_REQUEST)

        burguer = self.get_burguer(pk1)
        ingredient = self.get_ingredient(pk2)
        ingredients = burguer.ingredientes.all()

        if ingredient == 0:
            return Response('No Existe ese ingrediente', status=status.HTTP_404_NOT_FOUND)
        elif burguer == 0:
            return Response('No Existe esa hamburguesa', status=status.HTTP_404_NOT_FOUND)
        elif ingredient in ingredients:
            return Response('Ya existe ese ingrediente en la hamburguesa', status=status.HTTP_400_BAD_REQUEST)
        else:
            burguer.ingredientes.add(ingredient)
            return Response("se ha agregado", status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk1, pk2, format=None):
        try:
            pk1 = int(pk1)
        except:
            return Response('id hamburguesa invalido', status=status.HTTP_400_BAD_REQUEST)
        try:
            pk2 = int(pk2)
        except:
            return Response('id ingrediente invalido', status=status.HTTP_400_BAD_REQUEST)
        
        burguer = self.get_burguer(pk1)
        ingredient = self.get_ingredient(pk2)
        ingredients = burguer.ingredientes.all()
        print(ingredients)
        if ingredient == 0:
            return Response('No Existe ese ingrediente', status=status.HTTP_404_NOT_FOUND)
        elif burguer == 0:
            return Response('No Existe esa hamburguesa', status=status.HTTP_404_NOT_FOUND)
        elif not ingredient in ingredients:
            return Response('No existe ese ingrediente en la hamburguesa', status=status.HTTP_404_NOT_FOUND)
        else:
            burguer.ingredientes.remove(ingredient)
            return Response("se ha removido exitosamente", status=status.HTTP_200_OK)
