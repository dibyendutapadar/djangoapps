from django.shortcuts import render, redirect
from .forms import CrossingForm, DirectionForm
import requests
from datetime import datetime, timedelta
from django.utils import timezone
import json
from threading import Timer

crossing_data = {
    'crossing_location': None,
    'number_of_directions': None,
    'signal_cycle_time': None,
    'directions': []
}


def get_crossing(request):
    if request.method == 'POST':
        form = CrossingForm(request.POST)
        if form.is_valid():
            crossing_data['crossing_location'] = form.cleaned_data['crossing_location']
            crossing_data['number_of_directions'] = form.cleaned_data['number_of_directions']
            crossing_data['signal_cycle_time'] = form.cleaned_data['signal_cycle_time']
            return redirect('get_directions')
    else:
        form = CrossingForm()
    
    return render(request, 'get_crossing.html', {'form': form})




def get_directions(request):
    if request.method == 'POST':
        direction_forms = [DirectionForm(request.POST, prefix=str(x),initial={'to_location': crossing_data['crossing_location']}) for x in range(crossing_data['number_of_directions'])]
        if all([form.is_valid() for form in direction_forms]):
            crossing_data['directions'] = [form.cleaned_data for form in direction_forms]
            print(crossing_data['directions'])
            return redirect('traffic_signal_simulation')
    else:
        direction_forms = [DirectionForm(prefix=str(x),initial={'to_location': crossing_data['crossing_location']}) for x in range(crossing_data['number_of_directions'])]
        # for form in direction_forms:
        #     form.fields['to_location'].disabled = True
    context={
        'direction_forms': direction_forms,
        'crossing_location': crossing_data['crossing_location']
    }

    return render(request, 'get_directions.html', context)



def update_traffic_data():
    # Bing Maps API Key
    api_key = 'Ah8vU7MSfvjmIDk4YQdsOVI7IlPFAFbolbfUxPnW4Xloujt5qA20h5OyAyk7cnLc'

    # Update traffic data for each direction
    for direction in crossing_data['directions']:
        from_location = direction['from_location']
        to_location = direction['to_location']
        
        # Construct the API request
        url = f"http://dev.virtualearth.net/REST/V1/Routes?wp.0={from_location}&wp.1={to_location}&key={api_key}"
        
        # Make the API call
        response = requests.get(url)
        data = response.json()

        # Extract travelDurationTraffic and update the direction data
        direction['travelDurationTraffic'] = data['resourceSets'][0]['resources'][0]['travelDurationTraffic']

    # Calculate total traffic duration to determine weight
    total_duration = sum(direction['travelDurationTraffic'] for direction in crossing_data['directions'])
    
    # Calculate signal time allocation based on traffic duration
    for direction in crossing_data['directions']:
        traffic_weight = direction['travelDurationTraffic'] / total_duration
        direction['signal_time'] = round(crossing_data['signal_cycle_time'] * traffic_weight)

def traffic_signal_simulation(request):
    # Update traffic data
    update_traffic_data()
    
    # Data to be sent to the template
    context = {
        'crossing_data': crossing_data,
        'last_updated': datetime.now(),
        'refresh_time': 300  # Set refresh time to 5 minutes from now
    }
    
    # Render the simulation template
    return render(request, 'traffic_signal_simulation.html', context)