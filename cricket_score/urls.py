from django.urls import path
from .views import home, MatchCreateView, TeamCreateView, TournamentCreateView, add_players, start_match, player_autocomplete, matches_list,take_score,record_score, record_score_action

urlpatterns = [
    path('', home, name='home'),
    path('new-match/', MatchCreateView.as_view(), name='new_match'),
    path('add-team/', TeamCreateView.as_view(), name='add_team'),
    path('add-tournament/', TournamentCreateView.as_view(), name='add_tournament'),
    path('add-players/<int:pk>/', add_players, name='add_players'),
    path('start-match/<int:pk>/', start_match, name='start_match'),
    path('matches/', matches_list, name='matches_list'),
    path('player-autocomplete/', player_autocomplete, name='player_autocomplete'),
    path('take-score/<int:pk>/', take_score, name='take_score'),
    path('record-score/<int:match_id>/', record_score, name='record_score'),
    path('<int:match_id>/record_action/', record_score_action, name='record_score_action'),

]