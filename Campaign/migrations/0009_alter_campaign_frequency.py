# Generated by Django 3.2.13 on 2022-07-27 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0008_campaign_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='Frequency',
            field=models.CharField(choices=[('Weekly', 'Weekly'), ('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Once', 'Once'), ('Undefined', 'Undefined')], default='Undefined', max_length=20),
        ),
    ]
