# Generated by Django 3.2.7 on 2022-02-18 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Demo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.CharField(blank=True, max_length=35)),
                ('company', models.CharField(max_length=100)),
                ('timestamp', models.CharField(max_length=30)),
            ],
        ),
    ]