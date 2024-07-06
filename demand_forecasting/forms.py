from django import forms
from .models import ForecastingRequest

class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = ForecastingRequest
        fields = ['csv_file']

class ForecastingForm(forms.ModelForm):
    date_column = forms.ChoiceField(choices=[])
    demand_column = forms.ChoiceField(choices=[])
    date_format = forms.ChoiceField(
        choices=[('dd-mm-yyyy', 'dd-mm-yyyy'), ('dd-mmm-yyyy', 'dd-mmm-yyyy'), 
                 ('mm-dd-yyyy', 'mm-dd-yyyy'), ('yyyy-mm-dd', 'yyyy-mm-dd'), 
                 ('mmm dd, yyyy', 'mmm dd, yyyy'),('dd-mmm-yy','dd-mmm-yy'),('dd-mm-yy','dd-mm-yy'),
                 ('mm-dd-yy','mm-dd-yy'),('yyyy-mm-dd','yyyy-mm-dd'),('dd mmm yyyy','dd mmm yyyy'),('dd/mm/yy','dd/mm/yy')],
        widget=forms.Select(attrs={
            'placeholder': 'Select date format',
            'help_text': 'Select the date format that matches your data.'
        })
    )
    frequency = forms.ChoiceField(
        choices=[('D', 'D'), ('W', 'W'), ('M', 'M'), ('Q', 'Q')],
        required=False,
        help_text="Frequency of data."
    )

    class Meta:
        model = ForecastingRequest
        fields = ['date_column', 'date_format', 'demand_column', 'forecast_days', 'train_test_split']

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns', [])
        super(ForecastingForm, self).__init__(*args, **kwargs)
        self.fields['date_column'].choices = [(col, col) for col in columns]
        self.fields['demand_column'].choices = [(col, col) for col in columns]



class ExponentialSmoothingForm(forms.Form):
    trend = forms.ChoiceField(
        choices=[(None, 'None'), ('add', 'Additive'), ('mul', 'Multiplicative')],
        required=False,
        help_text="Type of trend component."
    )
    seasonal = forms.ChoiceField(
        choices=[(None, 'None'), ('add', 'Additive'), ('mul', 'Multiplicative')],
        required=False,
        help_text="Type of seasonal component."
    )
    seasonal_periods = forms.IntegerField(
        required=False,
        help_text="(int) The number of periods in a complete seasonal cycle, e.g., 4 for quarterly data or 7 for daily data with a weekly cycle.."
    )
    initialization_method = forms.ChoiceField(
        choices=[(None, 'None'), ('estimated', 'estimated'), ('heuristic', 'heuristic'), ('legacy-heuristic', 'legacy-heuristic'), ('known', 'known')],
        required=False,
        help_text="None defaults to the pre-0.12 behavior where initial values are passed as part of fit. If any of the other values are passed, then the initial values must also be set when constructing the model. If ‘known’ initialization is used, then initial_level must be passed, as well as initial_trend and initial_seasonal if applicable. Default is ‘estimated’. “legacy-heuristic” uses the same values that were used in statsmodels 0.11 and earlier."
    )
    damped_trend = forms.BooleanField(required=False)
    optimized = forms.BooleanField(required=False)
