from django.db import models

class Expense(models.Model):
    trip_name = models.CharField(max_length=100, blank=True)
    type_of_expense = models.CharField(max_length=100, blank=True)
    expense_from = models.CharField(max_length=100, blank=True)
    expense_to = models.CharField(max_length=100, blank=True)
    totalAmount = models.IntegerField(default=0)
    createDate = models.CharField(max_length=100, blank=True)
    createTime = models.CharField(max_length=100, blank=True)
    createdBy = models.IntegerField(default=0)
    updateDate = models.CharField(max_length=100, blank=True)
    updateTime = models.CharField(max_length=100, blank=True)
    updatedBy = models.IntegerField(default=0)
    remarks = models.TextField(blank=True)
    employeeId = models.IntegerField(default=0)
