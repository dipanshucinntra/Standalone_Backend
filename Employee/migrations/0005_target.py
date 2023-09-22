# Generated by Django 3.2.13 on 2022-11-15 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0004_targetqty_targetyr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('monthYear', models.CharField(blank=True, max_length=50)),
                ('qtr', models.IntegerField(default=0)),
                ('sale', models.FloatField(default=0)),
                ('sale_diff', models.FloatField(default=0)),
                ('CreatedDate', models.CharField(blank=True, max_length=20)),
                ('UpdatedDate', models.CharField(blank=True, max_length=20)),
                ('SalesPersonCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', to_field='SalesEmployeeCode')),
                ('YearTarget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='YearTargetTarget', to='Employee.targetyr')),
            ],
        ),
    ]