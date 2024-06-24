from django.db import models
from django.utils.timezone import now

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team, related_name='players')

    def __str__(self):
        return self.name

class Match(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('paused', 'Paused'),
        ('1st_innings_running', '1st Innings Running'),
        ('1st_innings_over', '1st Innings Over'),
        ('2nd_innings_running', '2nd Innings Running'),
        ('2nd_innings_over', '2nd Innings Over')
    ]
    name = models.CharField(max_length=100)
    team1 = models.ForeignKey(Team, related_name='matches_as_team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='matches_as_team2', on_delete=models.CASCADE)
    # add teams score over and wickets for wuick veiew
    overs = models.IntegerField()
    date = models.DateField(default=now)
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    umpires = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    toss_won_by = models.ForeignKey(Team, related_name='toss_won_matches', on_delete=models.SET_NULL, null=True, blank=True)
    first_batting_team = models.ForeignKey(Team, related_name='first_batting_matches', on_delete=models.SET_NULL, null=True, blank=True)
    second_batting_team = models.ForeignKey(Team, related_name='second_batting_matches', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return self.name
    
class MatchPlayer(models.Model):
    match = models.ForeignKey(Match, related_name='match_players', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='match_players', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='match_players', on_delete=models.CASCADE)


class Ball(models.Model):
    EXTRA_TYPES = [
        ('wide', 'Wide'),
        ('no_ball', 'No Ball'),
        ('bye', 'Bye'),
        ('leg_bye', 'Leg Bye'),
        ('penalty_runs', 'Penalty Runs')
    ]

    WICKET_TYPES = [
        ('bowled', 'Bowled'),
        ('caught', 'Caught'),
        ('lbw', 'LBW'),
        ('run_out', 'Run Out'),
        ('stumped', 'Stumped'),
        ('hit_wicket', 'Hit Wicket'),
        ('hit_ball_twice', 'Hit the Ball Twice'),
        ('obstructing_field', 'Obstructing the Field'),
        ('timed_out', 'Timed Out'),
        ('handled_ball', 'Handled the Ball')
    ]

    match = models.ForeignKey(Match, related_name='match', on_delete=models.CASCADE)
    innings = models.IntegerField(choices=[(1, '1st Innings'), (2, '2nd Innings')])
    over = models.IntegerField()
    over_ball = models.IntegerField()
    current_ball = models.DecimalField(max_digits=4, decimal_places=1,blank=True,null=True)
    next_ball = models.DecimalField(max_digits=4, decimal_places=1,default=0.1)
    batting_team = models.ForeignKey(Team, related_name='batting_balls', on_delete=models.CASCADE)
    bowling_team = models.ForeignKey(Team, related_name='bowling_balls', on_delete=models.CASCADE)
    batter = models.ForeignKey(Player, related_name='batter', on_delete=models.CASCADE)
    non_striker_batter = models.ForeignKey(Player, related_name='non_striker', on_delete=models.CASCADE)
    bowler = models.ForeignKey(Player, related_name='bowler', on_delete=models.CASCADE)
    batter_run = models.IntegerField(blank=True,null=True)
    extra_type = models.CharField(max_length=50,choices=EXTRA_TYPES, blank=True, null=True )
    extra_run = models.IntegerField(blank=True,null=True)
    is_extra = models.BooleanField(default=False)
    is_wicket = models.BooleanField(default=False)
    wicket_type = models.CharField(max_length=50,choices=WICKET_TYPES, blank=True, null=True)
    wicket_bowler = models.ForeignKey(Player, related_name='wicket_bowler', on_delete=models.CASCADE, blank=True, null=True)
    wicket_fielder = models.ForeignKey(Player, related_name='wicket_fielder', on_delete=models.CASCADE, blank=True, null=True)
    commentary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.match.name} - Inning {self.innings} - Over {self.over}.{self.over_ball}"    