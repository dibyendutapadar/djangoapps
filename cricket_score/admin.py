from django.contrib import admin
from .models import Tournament, Team, Player, Match, MatchPlayer, Ball

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'coach')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('teams',)


class MatchPlayerInline(admin.TabularInline):
    model = MatchPlayer
    extra = 0
    can_delete = False
    readonly_fields = ('player',)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'team1', 'team2', 'overs', 'date', 'tournament', 'description')
    list_filter = ('tournament',)
    search_fields = ('name', 'description')
    inlines = [MatchPlayerInline]


@admin.register(MatchPlayer)
class MatchPlayerAdmin(admin.ModelAdmin):
    list_display = ('match', 'team', 'player')
    list_filter = ('match', 'team')
    search_fields = ('match__name', 'team__name', 'player__name')


@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = ('match', 'innings', 'over', 'over_ball', 'current_ball', 'batting_team', 'bowling_team', 'batter', 'bowler', 'batter_run', 'is_extra', 'is_wicket')
    list_filter = ('match', 'innings', 'over', 'batting_team', 'bowling_team', 'is_extra', 'is_wicket')
    search_fields = ('match__name', 'batter__name', 'bowler__name', 'commentary')
