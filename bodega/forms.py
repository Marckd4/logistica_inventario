from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'fecha_venc': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_imp': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_inv': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }




class ExcelUploadForm(forms.Form):
    archivo_excel = forms.FileField(label="Selecciona un archivo Excel")
