from __future__ import unicode_literals

from django.db import models

from userprofile.models import Employee, UserProfile

import random


customer_type_choices = (
	('res', 'Residential'),
	('cmcl', 'Commercial'),
)

company_type_choices = (
	('hotel', 'Hotels & Resorts'),
	('it', 'IT Companies'),
	('co', 'Corporate Offices'),
	('fpu', 'Food Processing Units'),
	('go', 'Government Offices'),
)

salutation_choices = (
	('mr', 'Mr'),
	('mrs', 'Mrs'),
	('ms', 'Ms'),
)

def generate_customer_id():
	customer_id = 'PG_' + str(random.randint(0, 100000))
	while Customer.objects.filter(customer_id__iexact=customer_id).exists():
		customer_id = 'PG_' + str(random.randint(0, 100000))
	return customer_id

class Customer(models.Model):
	customer_id = models.CharField(primary_key=True, default=generate_customer_id, max_length=20)
	customer_type = models.CharField(max_length=5, choices=customer_type_choices, db_index=True)
	company_name = models.TextField()
	contact_person = models.CharField(max_length=100, null=True, blank=True)
	salutation = models.CharField(max_length=4, choices=salutation_choices)
	email = models.CharField(max_length=100, null=True, blank=True)
	city = models.TextField()
	pincode = models.CharField(max_length=20, null=True, blank=True)
	address = models.TextField(null=True, blank=True)
	mobile = models.CharField(max_length=100, null=True, blank=True)
	landline = models.CharField(max_length=100, null=True, blank=True)
	company_type = models.CharField(max_length=5, choices=company_type_choices, null=True, blank=True)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Customer_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Customer_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.customer_id

def generate_enquiry_id():
	enquiry_id = 'ENQ_' + str(random.randint(0, 100000))
	while Enquiry.objects.filter(enquiry_id__iexact=enquiry_id).exists():
		enquiry_id = 'ENQ_' + str(random.randint(0, 100000))
	return enquiry_id

enquiry_choices = (
	('f', 'Followup'),
	('c', 'Confirmed'),
	('n', 'Not Interested'),
	('i', 'Inspection'),
)

class EnquiryService(models.Model):
	service = models.CharField(max_length=30)

	def __str__(self):
		return self.service

class Enquiry(models.Model):
	customer = models.OneToOneField(Customer)
	enquiry_id = models.CharField(primary_key=True, default=generate_enquiry_id, max_length=20)
	enquiry_date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=5, choices=enquiry_choices)
	comments = models.TextField()
	reminder_to = models.ForeignKey(Employee, null=True, blank=True)
	amount = models.IntegerField(null=True, blank=True)
	status_date = models.DateField(null=True, blank=True)

	service_required = models.ForeignKey(EnquiryService, null=True, blank=True)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Enquiry_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Enquiry_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.enquiry_id

	class Meta:
		ordering = ['-enquiry_date']

class EnquiryLog(models.Model):
	enquiry = models.ForeignKey(Enquiry)
	status = models.CharField(max_length=5, choices=enquiry_choices)
	status_date = models.DateField(null=True, blank=True)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="EnquiryLog_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="EnquiryLog_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

def generate_contract_id():
	contract_id = 'PGCONT_' + str(random.randint(0, 100000))
	while Contract.objects.filter(contract_id__iexact=contract_id).exists():
		contract_id = 'PGCONT_' + str(random.randint(0, 100000))
	return contract_id

contract_type_choices = (
	('amc', 'AMC'),
	('s', 'Single'),
	('st', 'Short Term'),
)

contract_terms_choices = (
	('monthly', 'Monthly'),
	('100', '100% Advance'),
)

class Contract(models.Model):
	customer = models.ForeignKey(Customer, null=True, blank=True)
	enquiry = models.ForeignKey(Enquiry, null=True, blank=True)
	contract_id = models.CharField(primary_key=True, default=generate_contract_id, max_length=20)

	billing_company_name = models.TextField(null=True, blank=True)
	billing_address = models.TextField(null=True, blank=True)

	total_contract_amount = models.IntegerField(default=0)
	is_tax_applicable = models.BooleanField(default=False)
	tax_percentage = models.IntegerField(default=15)
	tax_amount = models.IntegerField(default=0)
	net_contract_amount = models.IntegerField(default=0)
	date = models.DateField(auto_now_add=True)

	contract_type = models.CharField(max_length=5, choices=contract_type_choices)

	contract_employee = models.ForeignKey(Employee, null=True, blank=True)

	schedule = models.CharField(max_length=50, null=True, blank=True)
	no_of_services = models.CharField(max_length=10, null=True, blank=True)

	description = models.TextField()

	terms = models.CharField(max_length=20, choices=contract_terms_choices, null=True, blank=True)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Contract_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="Contract_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.contract_id

invoice_status_choices = (
	('p', 'Pending'),
	('b', 'Billed'),
	('snp', 'Service Not Provided'),
)

collection_type_choices = (
	('cash', 'Cash'),
	('cheque', 'Cheque'),
	('online', 'Online'),
)

deposited_to_choices = (
	('iob', 'IOB-A29'),
)

class ContractInvoice(models.Model):
	customer = models.ForeignKey(Customer, null=True, blank=True)
	contract = models.ForeignKey(Contract, null=True, blank=True)

	invoice_no = models.IntegerField()
	invoice_date = models.DateField(null=True, blank=True)

	bill_amount = models.FloatField(null=True,blank=True)
	recieved_amount = models.FloatField(null=True,blank=True)
	tds_deducted = models.FloatField(null=True,blank=True)
	discount = models.FloatField(null=True,blank=True)
	balance_amount = models.FloatField(null=True,blank=True)

	status = models.CharField(max_length=3, choices=invoice_status_choices, default='p')

	collection_type = models.CharField(max_length=20, choices=collection_type_choices, default='cash')
	collection_date = models.DateField(null=True, blank=True)

	# Cheque
	cheque_no = models.TextField(blank=True)
	cheque_date = models.DateField(null=True, blank=True)

	# Online
	ref_no = models.TextField(blank=True)
	transfer_date = models.DateField(null=True, blank=True)

	paid_bank = models.TextField(blank=True)

	deposited_to = models.CharField(max_length=20, choices=deposited_to_choices, default='iob')
	deposited_date = models.DateField(null=True, blank=True)

	remarks = models.TextField(blank=True)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="ContractInvoice_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="ContractInvoice_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)

feedback_rating_choices = (
	('excellent', 'Excellent'),
	('satisfied', 'Satisfied'),
	('poor', 'POor'),
)

class CustomerContractFeedback(models.Model):
	customer = models.ForeignKey(Customer, null=True, blank=True)
	contract = models.ForeignKey(Contract, null=True, blank=True)

	person = models.CharField(max_length=30, null=True, blank=True)
	designation = models.CharField(max_length=30, null=True, blank=True)
	department = models.CharField(max_length=30, null=True, blank=True)
	mobile = models.CharField(max_length=20, null=True, blank=True)
	landline = models.CharField(max_length=20, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True)
	feedback = models.TextField(blank=True)
	rating = models.CharField(max_length=30, null=True, blank=True,choices=feedback_rating_choices)

	active = models.BooleanField(default=True)
	added_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="CustomerContractFeedback_added_by")
	edited_by = models.ForeignKey(UserProfile, null=True, blank=True, related_name="CustomerContractFeedback_edited_by")
	created_time = models.DateTimeField(auto_now_add=True)
	updated_time = models.DateTimeField(auto_now=True)



