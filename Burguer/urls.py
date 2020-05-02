from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from Burguer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hamburguesa', views.BurguerList.as_view()),
    path('hamburguesa/<str:pk>', views.BurguerDetail.as_view()),
    path('ingrediente', views.IngredientList.as_view()),
    path('ingrediente/<str:pk>', views.IngredientDetail.as_view()),
    path('hamburguesa/<str:pk1>/ingrediente/<str:pk2>', views.BurguerIngredient.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)