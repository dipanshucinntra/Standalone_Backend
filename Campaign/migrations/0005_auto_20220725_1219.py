# Generated by Django 3.2.13 on 2022-07-25 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0004_campaign_campaignsetid'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='MonthlyDate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='campaign',
            name='WeekDay',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
