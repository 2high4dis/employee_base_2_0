from django import forms
from .models import Employee


class DateInput(forms.DateInput):
    input_type = "date"


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'post', 'parent', 'hire_date', 'email']
        widgets = {
            'hire_date': DateInput(),
            'parent': forms.TextInput(),
        }
