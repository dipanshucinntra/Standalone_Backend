# Generated by Django 3.2.13 on 2022-07-29 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0011_alter_campaign_weekday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='MonthlyDate',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
