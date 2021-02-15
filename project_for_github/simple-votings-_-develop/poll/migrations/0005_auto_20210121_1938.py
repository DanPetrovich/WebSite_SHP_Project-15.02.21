# Generated by Django 3.1.5 on 2021-01-21 19:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20210117_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting_answers',
            name='voting_id',
        ),
        migrations.AlterField(
            model_name='votings',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='votings',
            name='name',
            field=models.TextField(default='Ellections'),
        ),
        migrations.AlterField(
            model_name='votings',
            name='question',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='voted_user_record',
        ),
        migrations.DeleteModel(
            name='voting_answers',
        ),
    ]
