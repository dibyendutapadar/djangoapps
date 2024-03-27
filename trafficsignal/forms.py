from django import forms

class CrossingForm(forms.Form):
    crossing_location = forms.CharField(label='Crossing Location', widget=forms.TextInput(attrs={'autocomplete': 'off'}))  # User input for location
    number_of_directions = forms.IntegerField(min_value=2, initial=2, label='Number of Directions')
    signal_cycle_time = forms.IntegerField(min_value=10,initial=60, label='Traffic Signal Cycle Time (seconds)')

class DirectionForm(forms.Form):
    from_location = forms.CharField(label='From', widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    to_location = forms.CharField(label='To', widget=forms.TextInput(attrs={'autocomplete': 'off'}))