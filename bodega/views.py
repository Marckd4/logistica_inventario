from django.shortcuts import render
from .models import Producto
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm

import pandas as pd
from django.contrib import messages
from .forms import ExcelUploadForm

from django.http import HttpResponse

from django.db.models import Q




def bodega_general(request):
    productos = Producto.objects.all()
    return render(request, 'bodega/bodega_general.html', {'productos': productos})



def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bodega_general')
    else:
        form = ProductoForm()
    return render(request, 'bodega/formulario_producto.html', {'form': form, 'titulo': 'Agregar Producto'})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('bodega_general')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'bodega/formulario_producto.html', {'form': form, 'titulo': 'Editar Producto'})



def importar_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_excel']
            try:
                df = pd.read_excel(archivo)

                # Validar que existan todas las columnas necesarias
                columnas_requeridas = [
                    'categoria', 'empresa', 'pasillo', 'ubicacion', 'cod_ean', 'cod_dun', 'cod_sistema',
                    'descripcion', 'unidad', 'pack', 'factorx', 'cajas', 'saldo', 'stock_fisico',
                    'observacion', 'fecha_venc', 'fecha_imp', 'contenedor', 'fecha_inv', 'encargado'
                ]

                if not all(col in df.columns for col in columnas_requeridas):
                    messages.error(request, "El archivo Excel no tiene todas las columnas requeridas.")
                    return redirect('importar_excel')

                for _, row in df.iterrows():
                    Producto.objects.create(
                        categoria=row['categoria'],
                        empresa=row['empresa'],
                        pasillo=row['pasillo'],
                        ubicacion=row['ubicacion'],
                        cod_ean=row['cod_ean'],
                        cod_dun=row['cod_dun'],
                        cod_sistema=row['cod_sistema'],
                        descripcion=row['descripcion'],
                        unidad=row['unidad'],
                        pack=row['pack'],
                        factorx=row['factorx'],
                        cajas=row['cajas'],
                        saldo=row['saldo'],
                        stock_fisico=row['stock_fisico'],
                        observacion=row.get('observacion', ''),
                        fecha_venc=row['fecha_venc'],
                        fecha_imp=row['fecha_imp'],
                        contenedor=row['contenedor'],
                        fecha_inv=row['fecha_inv'],
                        encargado=row['encargado'],
                    )

                messages.success(request, "Productos importados correctamente.")
                return redirect('bodega_general')

            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
    else:
        form = ExcelUploadForm()

    return render(request, 'bodega/importar_excel.html', {'form': form})





def exportar_excel(request):
    productos = Producto.objects.all().values(
        'categoria', 'empresa', 'pasillo', 'ubicacion', 'cod_ean', 'cod_dun', 'cod_sistema',
        'descripcion', 'unidad', 'pack', 'factorx', 'cajas', 'saldo', 'stock_fisico',
        'observacion', 'fecha_venc', 'fecha_imp', 'contenedor', 'fecha_inv', 'encargado'
    )
    df = pd.DataFrame(productos)

    # Crear respuesta Http con contenido Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=productos_exportados.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Productos')

    return response




def bodega_general(request):
    query = request.GET.get('q')
    productos = Producto.objects.all()

    if query:
        productos = productos.filter(
            Q(categoria__iexact=query) |
            Q(empresa__iexact=query) |
            Q(pasillo__iexact=query) |
            Q(ubicacion__iexact=query) |
            Q(cod_ean__iexact=query) |
            Q(cod_dun__iexact=query) |
            Q(cod_sistema__iexact=query) |
            Q(descripcion__iexact=query) |
            Q(unidad__iexact=query) |
            Q(pack__iexact=query) |
            Q(contenedor__iexact=query) |
            Q(encargado__iexact=query)
        )

    return render(request, 'bodega/bodega_general.html', {
        'productos': productos,
        'query': query or ''
    })
    
    


from django.db.models import Count, Sum

def resumen_general(request):
    productos = Producto.objects.all()

    resumen = {
        'total_productos': productos.count(),
        'total_cajas': productos.aggregate(Sum('cajas'))['cajas__sum'] or 0,
        'total_saldo': productos.aggregate(Sum('saldo'))['saldo__sum'] or 0,
        'total_stock_fisico': productos.aggregate(Sum('stock_fisico'))['stock_fisico__sum'] or 0,
        'por_categoria': productos.values('categoria').annotate(cantidad=Count('id')).order_by('-cantidad'),
        'por_empresa': productos.values('empresa').annotate(cantidad=Count('id')).order_by('-cantidad'),
    }

    return render(request, 'bodega/resumen_general.html', {'resumen': resumen})





