from django.db import models

class ScrumCall(models.Model):
    date = models.DateField(auto_now_add=True)
    time_taken = models.DurationField()

    def __str__(self):
        return f"Scrum Call on {self.date}"