from django import forms
from .models import Match, Team, Tournament

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['name', 'team1', 'team2', 'overs', 'date', 'tournament', 'description']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'city', 'coach']

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date']