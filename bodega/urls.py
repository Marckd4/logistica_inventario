from django.urls import path
from . import views

urlpatterns = [
    path('bodega/', views.bodega_general, name='bodega_general'),
    path('bodega/agregar/', views.crear_producto, name='crear_producto'),
    path('bodega/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('bodega/importar/', views.importar_excel, name='importar_excel'),
    path('bodega/exportar/', views.exportar_excel, name='exportar_excel'),
    path('resumen/', views.resumen_general, name='resumen_general'),



    
]

