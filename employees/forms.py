from django import forms
from .models import EmployeeUpdate, Document

class PersonalDetailsForm(forms.ModelForm):
    class Meta:
        model = EmployeeUpdate
        fields = [
            'email', 'phone_number', 'address', 'emergency_contact_name',
            'emergency_contact_number', 'emergency_contact_relationship'
        ]
        labels = {
            'email': 'Email',
            'phone_number': 'Phone Number',
            'address': 'Address',
            'emergency_contact_name': 'Emergency Contact Name',
            'emergency_contact_number': 'Emergency Contact Number',
            'emergency_contact_relationship': 'Emergency Contact Relationship'
        }

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
            'employee_id', 'document_type', 'document_description', 'document_path', 'validated'
        ]
        widgets = {
            'employee_id': forms.HiddenInput(),
            'validated': forms.HiddenInput(),
            'document_path': forms.FileInput(attrs={'accept': 'image/*,application/pdf'})
        }
        labels = {
            'document_path': 'Upload Document',
            'document_type': 'Document Type',
            'document_description': 'Document Description'
        }
    
    def __init__(self, *args, **kwargs):
        employee_id = kwargs.pop('employee_id', None)
        validated = kwargs.pop('validated', False)
        super(DocumentForm, self).__init__(*args, **kwargs)
        
        if employee_id is not None:
            self.fields['employee_id'].initial = employee_id

        self.fields['validated'].initial = False

    def save(self, commit=True):
        instance = super(DocumentForm, self).save(commit=False)
        # You can ensure validated is always set to False here
        instance.validated = False
        if commit:
            instance.save()
        return instance
