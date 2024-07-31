from django import forms

class UpdateTaskForm(forms.Form):
    task_id = forms.CharField(
        label='Task ID',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Task ID'})
    )
    assigned_to = forms.CharField(
        label='Assigned To',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Assigned Developer'})
    )
    status = forms.CharField(
        label='Status',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Status'})
    )
    blockers = forms.CharField(
        label='Blockers',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Blockers'})
    )
    comments = forms.CharField(
        label='Comments',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Comments'})
    )