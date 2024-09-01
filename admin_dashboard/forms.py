from django import forms
from departments.models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    department_id = forms.UUIDField(required=False, widget=forms.HiddenInput())
