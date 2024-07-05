import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.views import View
from .forms import UploadCSVForm, ForecastingForm, ExponentialSmoothingForm
from .models import ForecastingRequest
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from django_tables2 import RequestConfig
from .tables import PreviewTable
import os
from django.conf import settings
from sklearn.ensemble import AdaBoostRegressor
from xgboost import XGBRegressor
from keras.models import Sequential
from keras.layers import Dense, LSTM
import numpy as np
from dateutil import parser
from django_tables2 import RequestConfig
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATE_FORMAT_MAPPING = {
    'dd-mm-yyyy': '%d-%m-%Y',
    'dd-mmm-yyyy': '%d-%b-%Y',
    'mm-dd-yyyy': '%m-%d-%Y',
    'yyyy-mm-dd': '%Y-%m-%d',
    'mmm dd, yyyy': '%b %d, %Y',
    'dd-mmm-yy': '%d-%b-%y',
    'dd-mm-yy': '%d-%m-%y',
    'mm-dd-yy': '%m-%d-%y',
    'yyyy-mm-dd': '%Y-%m-%d',
    'dd mmm yyyy': '%d %b %Y',
    'dd/mm/yy': '%d/%m/%y',
    # Add more mappings as needed
}

def convert_to_strftime_format(user_format):
    return DATE_FORMAT_MAPPING.get(user_format.lower())

class UploadCSVView(View):
    def get(self, request):
        form = UploadCSVForm()
        return render(request, 'upload_csv.html', {'form': form})

    def post(self, request):
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            # Delete all existing CSVs
            media_path = os.path.join(settings.MEDIA_ROOT, 'csvs')
            if os.path.exists(media_path):
                for filename in os.listdir(media_path):
                    file_path = os.path.join(media_path, filename)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)

            # Save the new CSV
            csv_file = request.FILES['csv_file']
            file_path = os.path.join(media_path, csv_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            # Load the CSV into a DataFrame
            df = pd.read_csv(file_path)
            request.session['df'] = df.to_dict(orient='list')
            request.session['headers'] = df.columns.tolist()
            request.session['preview'] = df.head().to_dict(orient='records')

            return redirect('demand_forecasting:configure')
        return render(request, 'upload_csv.html', {'form': form})

class ConfigureForecastView(View):
    def get(self, request):
        headers = request.session.get('headers', [])
        preview_data = request.session.get('preview', [])
        form = ForecastingForm(columns=headers)

        df = pd.DataFrame(request.session.get('df'))
        preview_table = PreviewTable(df.to_dict('records'))
        df_html = df.head().to_html(classes='table table-striped')

        RequestConfig(request).configure(preview_table)

        return render(request, 'configure_forecast.html', {
            'form': form,
            'df_html': df_html
        })

    def post(self, request):
        headers = request.session.get('headers', [])
        df_dict = request.session.get('df')
        df = pd.DataFrame(df_dict)
        form = ForecastingForm(request.POST, columns=headers)

        if form.is_valid():
            date_column = form.cleaned_data['date_column']
            user_date_format = form.cleaned_data['date_format']
            date_format = convert_to_strftime_format(user_date_format)
            preview_data = request.session.get('preview', [])
            df_html = df.head().to_html(classes='table table-striped')
            preview_table = PreviewTable(preview_data)
            RequestConfig(request).configure(preview_table)

            if not date_format:
                return render(request, 'configure_forecast.html', {
                    'form': form,
                    'preview_table': preview_table,
                    'df_html': df_html,
                    'error': 'Could not convert the date format. Please ensure the date format is correct.'
                })

            demand_column = form.cleaned_data['demand_column']
            forecast_days = form.cleaned_data['forecast_days']
            train_test_split = form.cleaned_data['train_test_split']

            # Save the ForecastingRequest instance
            forecasting_request = ForecastingRequest.objects.create(
                csv_file='',
                date_column=date_column,
                date_format=date_format,
                demand_column=demand_column,
                forecast_days=forecast_days,
                train_test_split=train_test_split
            )

            request.session['forecasting_request_id'] = forecasting_request.id

            return redirect('demand_forecasting:results')

        preview_data = request.session.get('preview', [])
        preview_table = PreviewTable(preview_data)
        RequestConfig(request).configure(preview_table)

        return render(request, 'configure_forecast.html', {
            'form': form,
            'preview_table': preview_table,
            'df_html': df_html,
        })




class ForecastResultView(View):
    def get(self, request):
        last_request = ForecastingRequest.objects.last()
        if not last_request:
            return redirect('demand_forecasting:upload_csv')

        df_dict = request.session.get('df')
        df = pd.DataFrame(df_dict)
        date_column = last_request.date_column
        date_format = last_request.date_format
        demand_column = last_request.demand_column
        forecast_days = last_request.forecast_days
        train_test_split = last_request.train_test_split

        df[date_column] = pd.to_datetime(df[date_column], format=date_format)
        df = df.set_index(date_column)
        df = df[[demand_column]].dropna()

        if len(df) == 0:
            return render(request, 'results.html', {'error': 'The dataframe is empty after filtering.'})

        df[demand_column] = pd.to_numeric(df[demand_column], errors='coerce').fillna(0)

        split_idx = int(len(df) * (train_test_split/100))
        if split_idx == 0 or split_idx >= len(df):
            return render(request, 'results.html', {'error': 'The split index is out of bounds. Please check your data and split ratio.'})

        train, test = df[:split_idx], df[split_idx:]
        if len(train) == 0 or len(test) == 0:
            return render(request, 'results.html', {'error': 'Training or testing data is empty after the split.'})

        # Initialize the form with default values
        form = ExponentialSmoothingForm(initial={
            'trend': 'add',
            'seasonal': 'add',
            'seasonal_periods': 7,
            'initialization_method': None,
            'damped_trend': True,
            'optimized': True
        })

        context = self.get_forecast_context(train, test, df, demand_column, forecast_days, form, is_get=True, freq=df.index.freq)
        return render(request, 'results.html', context)

    def post(self, request):
        last_request = ForecastingRequest.objects.last()
        if not last_request:
            return redirect('demand_forecasting:upload_csv')

        df_dict = request.session.get('df')
        df = pd.DataFrame(df_dict)
        date_column = last_request.date_column
        date_format = last_request.date_format
        demand_column = last_request.demand_column
        forecast_days = last_request.forecast_days
        train_test_split = last_request.train_test_split

        df[date_column] = pd.to_datetime(df[date_column], format=date_format)
        df = df.set_index(date_column)
        df = df[[demand_column]].dropna()

        if len(df) == 0:
            return render(request, 'results.html', {'error': 'The dataframe is empty after filtering.'})

        df[demand_column] = pd.to_numeric(df[demand_column], errors='coerce').fillna(0)

        split_idx = int(len(df) * (train_test_split/100))
        print("Split_idx:",split_idx) #debugging
        if split_idx == 0 or split_idx >= len(df):
            return render(request, 'results.html', {'error': 'The split index is out of bounds. Please check your data and split ratio.'})

        train, test = df[:split_idx], df[split_idx:]
        if len(train) == 0 or len(test) == 0:
            return render(request, 'results.html', {'error': 'Training or testing data is empty after the split.'})

        form = ExponentialSmoothingForm(request.POST)

        if form.is_valid():
            context = self.get_forecast_context(train, test, df, demand_column, forecast_days, form, is_get=False, freq=df.index.freq)
            return render(request, 'results.html', context)
        else:
            context = self.get_forecast_context(train, test, df, demand_column, forecast_days, form, is_get=False, freq=df.index.freq)
            context['error'] = 'Invalid form input'
            return render(request, 'results.html', context)


    def get_forecast_context(self, train, test, df, demand_column, forecast_days, form, is_get, freq):
        if is_get:
            params = {
                'trend': 'add',
                'seasonal': 'add',
                'seasonal_periods': 7,
                'initialization_method': None,
                'damped_trend': True,
            }
            optimized = True
        else:
            params = {
                'trend': form.cleaned_data.get('trend') or 'add',
                'seasonal': form.cleaned_data.get('seasonal') or 'add',
                'seasonal_periods': form.cleaned_data.get('seasonal_periods') or 7,
                'damped_trend': form.cleaned_data.get('damped_trend'),
            }
            optimized = form.cleaned_data.get('optimized') or True


        model = ExponentialSmoothing(df[demand_column], **{k: v for k, v in params.items() if v is not None})
        fit = model.fit(optimized=optimized)

        # Historical forecast
        historical_forecast = fit.fittedvalues

        # Future forecast
        future_forecast_index = pd.date_range(start=df.index[-1], periods=forecast_days + 1, inclusive='right', freq=freq)[1:]
        future_forecast = fit.forecast(forecast_days)
        future_forecast = pd.Series(future_forecast, index=future_forecast_index)

        # Calculate KPIs for historical forecast
        error = round((historical_forecast - df[demand_column]).mean(), 2)
        mape = round(((historical_forecast - df[demand_column]).abs() / df[demand_column]).mean() * 100, 2)
        mae = round((historical_forecast - df[demand_column]).abs().mean(), 2)
        rmse = round(((historical_forecast - df[demand_column]) ** 2).mean() ** 0.5, 2)

        kpi_data = {
            'error': error,
            'mape': mape,
            'mae': mae,
            'rmse': rmse
        }

        # Difference table
        difference_df = pd.DataFrame({
            'Date': test.index,
            'Actual': test[demand_column],
            'Prediction': historical_forecast[test.index],
            'Difference': historical_forecast[test.index] - test[demand_column]
        })

        fig = px.line(df, x=df.index, y=demand_column, title='Exponential Smoothing Demand Forecast')
        fig.add_scatter(x=historical_forecast.index, y=historical_forecast.values, mode='lines', name='Historical Forecast', line=dict(color='red'))
        fig.add_scatter(x=future_forecast.index, y=future_forecast.values, mode='lines', name='Future Forecast', line=dict(color='green'))

        return {
            'form': form,
            'kpi_data': kpi_data,
            'plot': fig.to_html(full_html=False),
            'difference_table': difference_df.to_html(classes='table table-striped')
        }
