# Generated by Django 3.2.12 on 2022-05-31 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Opportunity', '0003_opportunity_u_fav'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='U_FAV',
            field=models.CharField(default='no', max_length=10),
        ),
    ]
