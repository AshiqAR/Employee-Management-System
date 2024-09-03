from django import forms
from django.utils import timezone
from .models import LeaveRequest, LeaveType, LeaveStatus

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        labels = {
            'leave_type': 'Leave Type',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Reason'
        }
        widgets = {
            'leave_type': forms.Select(choices=LeaveType.choices),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4})
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # start date is not in the past
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError('Start date cannot be in the past.')

        # end date is after the start date
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('End date must be greater than or equal to the start date.')

        return cleaned_data
    
    def save(self, commit=True, employee=None):
        """
        Save the leave request. Requires the employee instance.
        """
        if employee is None:
            raise ValueError("Employee must be provided to save the leave request.")

        leave_request = super().save(commit=False)
        leave_request.employee = employee  # Associate the leave request with the employee
        leave_request.status = LeaveStatus.PENDING
        leave_request.requested_at = timezone.now()

        if commit:
            leave_request.save()
        
        return leave_request
