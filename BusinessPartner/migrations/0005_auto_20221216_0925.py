# Generated by Django 3.2.13 on 2022-12-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusinessPartner', '0004_attachment_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesspartner',
            name='U_LEADID',
            field=models.CharField(blank=True, default='0', max_length=10),
        ),
        migrations.AddField(
            model_name='businesspartner',
            name='U_LEADNM',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]