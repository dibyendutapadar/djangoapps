from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ScrumCall
from .forms import UpdateTaskForm
from .utils import get_sprint_data, update_sprint_data, get_retrospective_data, get_developer_data, service
from collections import defaultdict, namedtuple
import logging
import json

# Configure logging
logger = logging.getLogger(__name__)

SPREADSHEET_ID = '12PyNj5irKjsm__GFLf8smKSc3qz4N87vZhV0SwoQBw0'
SPRINT_RANGE = 'Sprint Sheet!A2:M'
DEVELOPER_RANGE = 'Developer Sheet!A2:B'
RETRO_RANGE = 'Retrospective Sheet!A1:D'

def start_scrum_call(request):
    sprint_data = get_sprint_data(service, SPREADSHEET_ID, SPRINT_RANGE)
    developer_data = get_developer_data(service, SPREADSHEET_ID, DEVELOPER_RANGE)
    request.session['start_time'] = timezone.now().isoformat()  # Log start time
    return render(request, 'scrum_call.html', {'sprint_data': sprint_data, 'developer_data': developer_data})

def update_sprint_status(request):
    sprint_data = get_sprint_data(service, SPREADSHEET_ID, SPRINT_RANGE)
    developer_data = get_developer_data(service, SPREADSHEET_ID, DEVELOPER_RANGE)

    # Group tasks by developers
    tasks_by_developer = defaultdict(list)
    for row in sprint_data:
        while len(row) < 13:
            row.append('')
        tasks_by_developer[row[4]].append(row)  # Assuming Assigned To is the 5th column (index 4)

    # Sort developers alphabetically
    sorted_developers = sorted(tasks_by_developer.keys())

    if request.method == 'POST':
        updated_data = []
        for row in sprint_data:
            try:
                task_id = row[1]
                row[4] = request.POST.get(f'assigned_to_{task_id}', row[4])
                row[6] = request.POST.get(f'start_date_{task_id}', row[6])
                row[7] = request.POST.get(f'status_{task_id}', row[7])
                row[8] = request.POST.get(f'blockers_{task_id}', row[8])
                row[10] = request.POST.get(f'estimated_end_date_{task_id}', row[10])
                row[12] = request.POST.get(f'comments_{task_id}', row[12])
                row[9] = timezone.now().strftime("%Y-%m-%d")  # Update Last Status Update
                updated_data.append(row)
            except IndexError as e:
                logger.error(f"IndexError: {e} - Row data: {row}")
                return render(request, 'error.html', {'message': f"Error processing row: {row}"})

        update_sprint_data(service, SPREADSHEET_ID, SPRINT_RANGE, updated_data)

        # Calculate elapsed time and log it in the database
        start_time = timezone.datetime.fromisoformat(request.session['start_time'])
        end_time = timezone.now()
        elapsed_time = end_time - start_time
        ScrumCall.objects.create(date=end_time.date(), time_taken=elapsed_time)
        
        return redirect('scrum:show_analytics')

    context = {
        'tasks_by_developer': tasks_by_developer,
        'sorted_developers': sorted_developers,
        'developer_list': developer_data,
    }

    return render(request, 'update_sprint_status.html', context)

def show_analytics(request):
    sprint_data = get_sprint_data(service, SPREADSHEET_ID, SPRINT_RANGE)
    
    # Calculate total story points completed and in progress
    total_story_points_completed = sum(int(row[5]) for row in sprint_data if row[7] == 'Completed')
    total_story_points_in_progress = sum(int(row[5]) for row in sprint_data if row[7] == 'In progress')
    
    # Prepare data for developer-wise analytics
    DeveloperAnalytics = namedtuple('DeveloperAnalytics', ['tasks_completed', 'tasks_in_progress', 'tasks_not_started', 'tasks_blocked', 'total_story_points'])
    developer_analytics = defaultdict(lambda: DeveloperAnalytics(0, 0, 0, 0, 0))

    for row in sprint_data:
        assigned_to = row[4]
        status = row[7]
        story_points = int(row[5])

        if status == 'Completed':
            developer_analytics[assigned_to] = developer_analytics[assigned_to]._replace(
                tasks_completed=developer_analytics[assigned_to].tasks_completed + 1,
                total_story_points=developer_analytics[assigned_to].total_story_points + story_points
            )
        elif status == 'In progress':
            developer_analytics[assigned_to] = developer_analytics[assigned_to]._replace(
                tasks_in_progress=developer_analytics[assigned_to].tasks_in_progress + 1,
                total_story_points=developer_analytics[assigned_to].total_story_points + story_points
            )
        elif status == 'Not started':
            developer_analytics[assigned_to] = developer_analytics[assigned_to]._replace(
                tasks_not_started=developer_analytics[assigned_to].tasks_not_started + 1
            )
        elif status == 'Blocked':
            developer_analytics[assigned_to] = developer_analytics[assigned_to]._replace(
                tasks_blocked=developer_analytics[assigned_to].tasks_blocked + 1
            )

    # Prepare data for burndown chart
    burn_down_dates = [row[9] for row in sprint_data]  # Last Status Update dates
    burn_down_points = [int(row[5]) for row in sprint_data]  # Story Points

    # Prepare data for sprint time chart (last 7 records)
    scrum_calls = ScrumCall.objects.all().order_by('-date')[:7]
    sprint_dates = [call.date.strftime('%Y-%m-%d') for call in scrum_calls]
    sprint_times = [call.time_taken.total_seconds() / 60.0 for call in scrum_calls]  # Convert seconds to minutes

    context = {
        'total_story_points_completed': total_story_points_completed,
        'total_story_points_in_progress': total_story_points_in_progress,
        'developer_analytics': dict(developer_analytics),  # Convert defaultdict to dict
        'burn_down_dates': json.dumps(burn_down_dates),
        'burn_down_points': json.dumps(burn_down_points),
        'sprint_dates': json.dumps(sprint_dates),
        'sprint_times': json.dumps(sprint_times),
    }

    return render(request, 'analytics.html', context)

def show_retrospective(request):
    retrospective_data = get_retrospective_data(service, SPREADSHEET_ID, RETRO_RANGE)
    developer_data = get_developer_data(service, SPREADSHEET_ID, DEVELOPER_RANGE)

    if request.method == 'POST':
        updated_data = []
        for idx, row in enumerate(retrospective_data, start=1):
            row[2] = request.POST.get(f'assigned_to_{idx}', row[2])
            row[3] = request.POST.get(f'status_{idx}', row[3])
            updated_data.append(row)

        update_sprint_data(service, SPREADSHEET_ID, RETRO_RANGE, updated_data)
        return redirect('scrum:show_retrospective')

    context = {
        'retrospective_data': retrospective_data,
        'developer_list': developer_data,
    }
    return render(request, 'retrospective.html', context)

def end_scrum_call(request):
    if request.method == 'POST':
        time_taken = request.POST.get('time_taken')
        ScrumCall.objects.create(time_taken=time_taken)
        return redirect('scrum:show_scrum_call_times')


def show_scrum_call_times(request):
    scrum_calls = ScrumCall.objects.all()
    return render(request, 'scrum_call_times.html', {'scrum_calls': scrum_calls})