# Generated by Django 3.2.13 on 2022-11-15 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0003_auto_20220823_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Targetyr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Department', models.CharField(blank=True, max_length=50)),
                ('StartYear', models.IntegerField(default=0)),
                ('EndYear', models.IntegerField(default=0)),
                ('YearTarget', models.BigIntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('CreatedDate', models.CharField(blank=True, max_length=20)),
                ('UpdatedDate', models.CharField(blank=True, max_length=20)),
                ('SalesPersonCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', to_field='SalesEmployeeCode')),
                ('reportingTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportingToTargetyr', to='Employee.employee', to_field='SalesEmployeeCode')),
            ],
        ),
        migrations.CreateModel(
            name='Targetqty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.BigIntegerField(default=0)),
                ('q2', models.BigIntegerField(default=0)),
                ('q3', models.BigIntegerField(default=0)),
                ('q4', models.BigIntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('CreatedDate', models.CharField(blank=True, max_length=20)),
                ('UpdatedDate', models.CharField(blank=True, max_length=20)),
                ('SalesPersonCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', to_field='SalesEmployeeCode')),
                ('YearTarget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.targetyr')),
                ('reportingTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportingToTargetqty', to='Employee.employee', to_field='SalesEmployeeCode')),
            ],
        ),
    ]
