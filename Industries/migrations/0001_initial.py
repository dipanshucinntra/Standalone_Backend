# Generated by Django 3.2.7 on 2022-02-18 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Industries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IndustryDescription', models.CharField(blank=True, max_length=200)),
                ('IndustryName', models.CharField(blank=True, max_length=100)),
                ('IndustryCode', models.CharField(blank=True, max_length=5)),
            ],
        ),
    ]
