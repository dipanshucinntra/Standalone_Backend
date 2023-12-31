# Generated by Django 3.2.13 on 2022-10-06 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lead', '0009_delete_casetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('File', models.CharField(blank=True, max_length=150)),
                ('CreateDate', models.CharField(blank=True, max_length=100)),
                ('CreateTime', models.CharField(blank=True, max_length=100)),
                ('UpdateDate', models.CharField(blank=True, max_length=100)),
                ('UpdateTime', models.CharField(blank=True, max_length=100)),
                ('LeadId', models.IntegerField(default=0)),
            ],
        ),
    ]
