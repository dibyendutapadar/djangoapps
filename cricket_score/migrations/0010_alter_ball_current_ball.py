# Generated by Django 4.2.11 on 2024-06-14 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket_score', '0009_ball_next_ball'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ball',
            name='current_ball',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
    ]
