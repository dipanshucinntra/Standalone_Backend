# Generated by Django 3.2.13 on 2022-12-02 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0013_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='junk',
            field=models.IntegerField(default='0'),
        ),
    ]