# Generated by Django 3.2.7 on 2022-02-18 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Employee', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chatter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Message', models.CharField(blank=True, max_length=250)),
                ('Lead_Id', models.CharField(blank=True, max_length=10)),
                ('Emp_Id', models.CharField(blank=True, max_length=10)),
                ('Emp_Name', models.CharField(blank=True, max_length=50)),
                ('UpdateDate', models.CharField(blank=True, max_length=100)),
                ('UpdateTime', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(blank=True, max_length=60)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('companyName', models.CharField(blank=True, max_length=100)),
                ('numOfEmployee', models.IntegerField(default='0')),
                ('turnover', models.CharField(blank=True, max_length=100)),
                ('source', models.CharField(blank=True, max_length=100)),
                ('contactPerson', models.CharField(blank=True, max_length=20)),
                ('designation', models.CharField(blank=True, max_length=50)),
                ('phoneNumber', models.CharField(blank=True, max_length=20)),
                ('message', models.CharField(blank=True, max_length=100)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('productInterest', models.CharField(blank=True, max_length=100)),
                ('timestamp', models.CharField(blank=True, max_length=60)),
                ('assignedTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignedTo', to='Employee.employee')),
                ('employeeId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.employee')),
            ],
        ),
    ]
