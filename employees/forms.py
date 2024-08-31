from django import forms
from .models import EmployeeUpdate, Document

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeUpdate
        fields = [
            'email', 'phone_number', 'address', 'emergency_contact_name',
            'emergency_contact_number', 'emergency_contact_relationship'
        ]

class BankDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeUpdate
        fields = [
            'bank_name', 'bank_account_number', 'ifsc_code', 'bank_branch'
        ]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'document_type', 'document_description', 'document_path'
        ]