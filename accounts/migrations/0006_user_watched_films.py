# Generated by Django 3.0.3 on 2020-03-02 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_auto_20200302_1954'),
        ('accounts', '0005_remove_user_watched_films'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watched_films',
            field=models.ManyToManyField(to='films.Film'),
        ),
    ]
