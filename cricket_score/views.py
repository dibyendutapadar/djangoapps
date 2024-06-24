from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from .forms import MatchForm, TeamForm, TournamentForm
from .models import Match, Team, Tournament, Player, MatchPlayer, Ball
from django.db.models import Sum, Count, Max, Q
from decimal import Decimal





class MatchCreateView(CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'new_match.html'
    success_url = '/add-players/'

    def get_success_url(self):
        return reverse('add_players', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_form'] = TeamForm()
        context['tournament_form'] = TournamentForm()
        return context

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'add_team.html'
    success_url = reverse_lazy('new_match')

class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'add_tournament.html'
    success_url = reverse_lazy('new_match')

# Create your views here.

def home(request):
    return render(request, 'cricket_home.html')


def add_players(request, pk):
    match = Match.objects.get(pk=pk)
    team1 = match.team1
    team2 = match.team2

    if request.method == 'POST':
        for i in range(1, 12):
            player_name = request.POST.get(f'team1_player{i}')
            if player_name:
                player, created = Player.objects.get_or_create(name=player_name)
                MatchPlayer.objects.create(match=match, team=team1, player=player)

            player_name = request.POST.get(f'team2_player{i}')
            if player_name:
                player, created = Player.objects.get_or_create(name=player_name)
                MatchPlayer.objects.create(match=match, team=team2, player=player)

        return redirect('start_match', pk=match.pk)

    context = {
        'match': match,
        'team1': team1,
        'team2': team2
    }
    return render(request, 'add_players.html', context)

def start_match(request, pk):
    match = Match.objects.get(pk=pk)
    match_players = MatchPlayer.objects.filter(match=match)
    context = {'match': match, 'match_players': match_players}
    return render(request, 'start_match.html', context)


def take_score(request, pk):
    match = Match.objects.get(pk=pk)
    if request.method == 'POST':
        umpires = request.POST.get('umpires')
        location = request.POST.get('location')
        toss_won_by_id = request.POST.get('toss_won_by')
        first_batting_team_id = request.POST.get('first_batting_team')
        second_batting_team_id = match.team2.id if first_batting_team_id == match.team1.id else match.team1.id

        match.umpires = umpires
        match.location = location
        match.toss_won_by_id = toss_won_by_id
        match.first_batting_team_id = first_batting_team_id
        match.second_batting_team_id = second_batting_team_id
        match.save()

        return redirect('record_score', pk=match.pk)

    context = {'match': match}
    return render(request, 'take_score.html', context)

def matches_list(request):
    matches = Match.objects.all()
    context = {'matches': matches}
    return render(request, 'matches.html', context)

def player_autocomplete(request):
    team_id = request.GET.get('team_id')
    query = request.GET.get('query', '')

    if team_id and query:
        players = Player.objects.filter(teams__id=team_id, name__icontains=query)
        player_names = [player.name for player in players]
        return JsonResponse(player_names, safe=False)

    return JsonResponse([], safe=False)

def record_score(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    balls = Ball.objects.filter(match=match)

    # Calculate overview details
    first_batting_team = match.first_batting_team
    second_batting_team = match.second_batting_team

    first_batting_stats = balls.filter(batting_team=first_batting_team).aggregate(
        total_runs=Sum('batter_run') + Sum('extra_run'),
        total_wickets=Count('id', filter=Q(is_wicket=True)),
        max_ball=Max('current_ball')
    )
    second_batting_stats = balls.filter(batting_team=second_batting_team).aggregate(
        total_runs=Sum('batter_run') + Sum('extra_run'),
        total_wickets=Count('id', filter=Q(is_wicket=True)),
        max_ball=Max('current_ball')
    )

    live_balls = balls.order_by('-current_ball')[:10]
    last_ball = balls.last()
    current_batter=last_ball.batter
    current_non_striker=last_ball.non_striker_batter

    if request.method == 'POST' and match.status == 'not_started':
        batter_id = request.POST.get('batter')
        non_striker_id = request.POST.get('non_striker')
        bowler_id = request.POST.get('bowler')

        batter = get_object_or_404(Player, id=batter_id)
        non_striker = get_object_or_404(Player, id=non_striker_id)
        bowler = get_object_or_404(Player, id=bowler_id)

        Ball.objects.create(
            match=match,
            innings=1,
            over=0,
            over_ball=0,
            batting_team=first_batting_team,
            bowling_team=second_batting_team,
            batter=batter,
            non_striker_batter=non_striker,
            bowler=bowler,
            extra_type=None,
            is_extra=False,
            is_wicket=False,
            commentary="Match started"
        )

        match.status = '1st_innings_running'
        match.save()

    context = {
        'match': match,
        'first_batting_stats': first_batting_stats,
        'second_batting_stats':second_batting_stats,
        'live_balls': live_balls,
        'balls':balls,
        'last_ball':last_ball,
        'current_batter':current_batter,
        'current_non_striker':current_non_striker
    }
    return render(request, 'record_score.html', context)

def record_score_action(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    action = request.POST.get('action')
    if not action:
        return HttpResponse("Invalid action", status=400)
    
    last_ball = Ball.objects.filter(match=match).order_by('-current_ball').first()
    if not last_ball:
        return HttpResponse("No previous ball found", status=400)
    
    new_ball = Ball(
        match=match,
        innings=last_ball.innings,
        over=last_ball.over,
        over_ball=last_ball.over_ball + 1 if last_ball.over_ball < 5 else 0,
        current_ball=last_ball.current_ball + Decimal('0.1') if last_ball.over_ball < 5 else Decimal(last_ball.over + 1),
        batting_team=last_ball.batting_team,
        bowling_team=last_ball.bowling_team,
        batter=last_ball.batter,
        non_striker_batter=last_ball.non_striker_batter,
        bowler=last_ball.bowler,
        batter_run=0,
        extra_run=0,
        is_extra=False,
        is_wicket=False
    )

    # Update the new_ball based on the action
    if action.isdigit():
        new_ball.batter_run = int(action)
    elif action == 'B':
        new_ball.is_extra = True
        new_ball.extra_run = 1
    elif action == 'LB':
        new_ball.is_extra = True
        new_ball.extra_run = 1
    elif action == 'Wd':
        new_ball.is_extra = True
        new_ball.extra_run = 1
    elif action == 'NB':
        new_ball.is_extra = True
        new_ball.extra_run = 1
    elif action == 'Out':
        new_ball.is_wicket = True
    
    new_ball.save()
    return redirect('record_score', match_id=match.id)