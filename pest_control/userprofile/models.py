from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

import random

user_type_choices = (
	('staff', 'Staff'),
	('admin', 'Admin'),
)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	full_name = models.CharField(max_length=100, null=True, blank=True)
	gender = models.CharField(max_length=10, null=True, blank=True)
	dob = models.DateField(null=True, blank=True)
	father = models.CharField(max_length=100, null=True, blank=True)
	mother = models.CharField(max_length=100, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True)
	present_address = models.TextField(blank=True)
	permanent_address = models.TextField(blank=True)
	mobile = models.CharField(max_length=15, null=True, blank=True)
	landline = models.CharField(max_length=15, null=True, blank=True)
	maritial_status = models.CharField(max_length=10, null=True, blank=True)
	user_type = models.CharField(max_length=10, choices=user_type_choices)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey('self', null=True, blank=True, related_name="UserProfile_added_by")
	edited_by = models.ForeignKey('self', null=True, blank=True, related_name="UserProfile_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username

def generate_employee_id():
	employee_id = 'PHIPL_' + str(random.randint(0, 100000))
	while Employee.objects.filter(employee_id__iexact=employee_id).exists():
		employee_id = 'PHIPL_' + str(random.randint(0, 100000))
	return employee_id

employee_type_choices = (
	('m', 'Manager'),
	('am', 'Assistant Manager'),
	('se', 'Sales Executive'),
	('cs', 'Customer Support'),
	('oa', 'Office Admin'),
)

class Employee(models.Model):
	userprofile = models.OneToOneField(UserProfile)
	employee_id = models.CharField(primary_key=True, default=generate_employee_id, max_length=20)
	employee_type = models.CharField(max_length=3, choices=employee_type_choices)
	date_joined = models.DateField(null=True, blank=True)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Employee_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Employee_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.employee_id
