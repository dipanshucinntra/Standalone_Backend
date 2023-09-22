# Generated by Django 4.0.3 on 2022-09-26 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.CharField(blank=True, max_length=150)),
                ('LinkType', models.CharField(blank=True, max_length=100)),
                ('Caption', models.CharField(blank=True, max_length=500)),
                ('LinkID', models.IntegerField(default=0)),
                ('CreateDate', models.CharField(blank=True, max_length=100)),
                ('CreateTime', models.CharField(blank=True, max_length=100)),
                ('UpdateDate', models.CharField(blank=True, max_length=100)),
                ('UpdateTime', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
