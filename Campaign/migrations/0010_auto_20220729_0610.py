# Generated by Django 3.2.13 on 2022-07-29 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0009_alter_campaign_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='Frequency',
            field=models.CharField(default='Undefined', max_length=255),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='QualityResponse',
            field=models.CharField(default='Undefined', max_length=255),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='Type',
            field=models.CharField(default='Undefined', max_length=255),
        ),
    ]