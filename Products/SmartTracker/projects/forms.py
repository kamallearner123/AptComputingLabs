from django import forms
from .models import WorkTaskModel, EmployeeModel

class WorkTaskForm(forms.ModelForm):
    class Meta:
        model = WorkTaskModel
        fields = ['project', 'title', 'description', 'assigned_to', 'status', 'start_date', 'end_date']
        widgets = {
            'assigned_to': forms.Select()  # Ensure this is a dropdown of employee IDs
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = EmployeeModel.objects.filter(is_active=True)