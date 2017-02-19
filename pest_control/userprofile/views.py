from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User

from customer.models import customer_type_choices, company_type_choices, salutation_choices, enquiry_choices, Enquiry, EnquiryService, Customer, contract_type_choices, contract_terms_choices, Contract
from userprofile.models import UserProfile, Employee, employee_type_choices

from pest_control.utils import generate_bill

import datetime
import json

def MyPaginator(query_set, page):
	paginator = Paginator(query_set, 25)

	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)

	return data

def check_username_availabilty(request):
	response = {}

	username = request.GET.get('username', '')

	if not username or User.objects.filter(username__iexact=username).exists():
		response.update({'status':False})
	else:
		response.update({'status':True})

	return HttpResponse(
		json.dumps(response),
		content_type='application/json'
	)

@login_required
def dashboard(request):
	response = {}
	if 'contract_created' in request.GET and request.GET['contract_created']:
		try:
			contract = get_object_or_404(Contract, contract_id=request.GET['contract_created'])
		except:
			pass
		else:
			response.update({'contract':contract})

	return render(request, 'userprofile/dashboard.html', response)

@login_required
def add_enquiry(request):
	response = {}
	response.update({'customer_type_choices':customer_type_choices})
	response.update({'company_type_choices':company_type_choices})
	response.update({'salutation_choices':salutation_choices})
	response.update({'enquiry_choices':enquiry_choices})
	response.update({'services':EnquiryService.objects.all()})

	if request.method == 'POST':

		if 'enquiry_id' in request.POST and request.POST['enquiry_id']:
			enquiry = get_object_or_404(Enquiry, enquiry_id=request.POST['enquiry_id'])
		else:
			enquiry = None

		# initialize customer object
		if enquiry:
			customer = enquiry.customer
		else:
			customer = Customer()

		customer.customer_type = request.POST['customer_type']
		if customer.customer_type == 'cmcl':
			customer.company_name = request.POST.get('company_name', '')
			customer.company_type = request.POST.get('company_type', '')
		else:
			customer.company_name = ''
			customer.company_type = ''

		customer.salutation = request.POST['salutation']
		customer.contact_person = request.POST['contact_person']
		customer.address = request.POST.get('address', '')
		customer.pincode = request.POST.get('pincode', '')
		customer.mobile = request.POST.get('mobile', '')
		customer.landline = request.POST.get('landline', '')
		customer.email = request.POST.get('email', '')

		customer.save()

		# initialize enquiry object
		if not enquiry:
			enquiry = Enquiry()

		enquiry.customer = customer
		enquiry.enquiry_date = datetime.datetime.strptime(request.POST['enquiry_date'], '%m/%d/%Y')
		enquiry.status = request.POST.get('status', '')

		if enquiry.status == 'c':
			enquiry.amount = request.POST.get('amount', '')
			enquiry.service_required = get_object_or_404(EnquiryService, id=request.POST['service'])

		else:
			enquiry.status_date = datetime.datetime.strptime(request.POST['status_date'], '%m/%d/%Y')

		enquiry.comments = request.POST.get('comments', '')

		try:
			enquiry.save()
		except:
			customer.delete()
			response.update({'error':True})
		else:
			response.update({'success':True})
			if enquiry.status == 'c':
				return HttpResponseRedirect('/enquiry/' + enquiry.enquiry_id + '/contract/')

	return render(request, 'userprofile/add_enquiry.html', response)

@login_required
def edit_enquiry(request, enq_id):
	response = {}
	response.update({'customer_type_choices':customer_type_choices})
	response.update({'company_type_choices':company_type_choices})
	response.update({'salutation_choices':salutation_choices})
	response.update({'enquiry_choices':enquiry_choices})
	response.update({'services':EnquiryService.objects.all()})

	try:
		enquiry = Enquiry.objects.select_related('customer').get(enquiry_id=enq_id)
	except:
		raise Http404()
		
	response.update({'enquiry':enquiry})
	return render(request, 'userprofile/add_enquiry.html', response)

@login_required
def enquiry_report(request):
	response = {}
	enquiries = Enquiry.objects.select_related('customer').all()
	page = request.GET.get('page', '1')
	if 'enquiry_date_range' in request.GET and request.GET['enquiry_date_range']:
		enquiry_date_range = request.GET['enquiry_date_range']
		enquiry_date_range = enquiry_date_range.split('-')

		from_date = datetime.datetime.strptime(enquiry_date_range[0].replace(" ", ""), '%m/%d/%Y')
		to_date = datetime.datetime.strptime(enquiry_date_range[1].replace(" ", ""), '%m/%d/%Y')

		enquiries = enquiries.filter(enquiry_date__range=(from_date, to_date + datetime.timedelta(days=1)))
	
	enquiries = MyPaginator(enquiries, page)

	response.update({'enquiries':enquiries})
	return render(request, 'userprofile/enquiry_report.html', response)

@login_required
def add_contract(request, enq_id):
	response = {}
	response.update({'services':EnquiryService.objects.all()})
	response.update({'employees':Employee.objects.all()})
	response.update({'contract_type_choices':contract_type_choices})
	response.update({'contract_terms_choices':contract_terms_choices})

	try:
		enquiry = Enquiry.objects.select_related('customer').get(enquiry_id=enq_id)
	except:
		raise Http404()

	response.update({'enquiry':enquiry})

	if request.method == 'POST':

		enquiry.service_required = get_object_or_404(EnquiryService, id=request.POST['service'])
		enquiry.save()

		# initialize contract object
		contract = Contract()
		contract.customer = enquiry.customer
		contract.enquiry = enquiry
		contract.billing_company_name = request.POST['billing_company_name']
		contract.billing_address = request.POST['billing_address']

		contract.total_contract_amount = request.POST['total_contract_amount']
		contract.is_tax_applicable = True if 'is_tax_applicable' in request.POST else False

		if contract.is_tax_applicable:
			contract.tax_amount = request.POST['tax_amount']

		contract.net_contract_amount = request.POST['net_contract_amount']
		contract.date = datetime.datetime.strptime(request.POST['date'], '%m/%d/%Y')
		contract.contract_type = request.POST['contract_type']

		try:
			contract_employee = get_object_or_404(Employee, employee_id=request.POST['contract_employee'])
		except:
			contract_employee = None

		contract.contract_employee = contract_employee
		contract.schedule = request.POST['schedule']
		contract.no_of_services = request.POST['no_of_services']
		contract.description = request.POST['description']
		contract.terms = request.POST['terms']
		contract.save()

		if contract.contract_type == 's':
			generate_bill(contract=contract)

		return HttpResponseRedirect('/dashboard/?contract_created=' + str(contract.contract_id))
		response.update({'success':True})

	return render(request, 'userprofile/add_contract.html', response)


@login_required
def contract_report(request):
	response = {}
	contracts = Contract.objects.select_related('customer','enquiry').all()
	page = request.GET.get('page', '1')
	if 'contract_date_range' in request.GET and request.GET['contract_date_range']:
		contract_date_range = request.GET['contract_date_range']
		contract_date_range = contract_date_range.split('-')

		from_date = datetime.datetime.strptime(contract_date_range[0].replace(" ", ""), '%m/%d/%Y')
		to_date = datetime.datetime.strptime(contract_date_range[1].replace(" ", ""), '%m/%d/%Y')

		contracts = contracts.filter(date__range=(from_date, to_date + datetime.timedelta(days=1)))

		response.update({'from_date':from_date})
		response.update({'to_date':to_date})
	
	contracts = MyPaginator(contracts, page)

	response.update({'contracts':contracts})
	return render(request, 'userprofile/contract_report.html', response)

@login_required
def contract_details(request, contract_id):
	response = {}

	try:
		contract = Contract.objects.select_related('customer','enquiry').prefetch_related('customercontractfeedback_set', 'contractinvoice_set').get(contract_id=contract_id)
	except:
		raise Http404()

	pending_invoices = contract.contractinvoice_set.filter(status='p')
	billed_invoices = contract.contractinvoice_set.exclude(status='p')

	response.update({'contract':contract})
	response.update({'pending_invoices':pending_invoices})
	response.update({'billed_invoices':billed_invoices})

	return render(request, 'userprofile/contract_details.html', response)

@login_required
def add_employee(request):
	response = {}
	response.update({'employee_type_choices':employee_type_choices})

	if request.method == 'POST':

		username = request.POST['username']
		password = request.POST['password']

		try:
			User.objects.get(username__iexact=username)
		except:
			user = User()
			user.username = username
			user.set_password(password)
			user.save()
		else:
			response.update({'error':True})
			response.update({'error_message':'Username already exists, please use another username'})
			return render(request, 'userprofile/add_employee.html', response)

		# initialize userprofile object
		userprofile = UserProfile()
		userprofile.user = user
		userprofile.full_name = request.POST.get('full_name', '')
		userprofile.gender = request.POST.get('gender', '')
		dob = request.POST.get('dob', '')
		if dob:
			userprofile.dob = datetime.datetime.strptime(dob, '%m/%d/%Y')
		userprofile.father = request.POST.get('father', '')
		userprofile.mother = request.POST.get('mother', '')
		userprofile.email = request.POST.get('email', '')
		userprofile.present_address = request.POST.get('present_address', '')
		userprofile.permanent_address = request.POST.get('permanent_address', '')
		userprofile.mobile = request.POST.get('mobile', '')
		userprofile.landline = request.POST.get('landline', '')
		userprofile.maritial_status = request.POST.get('maritial_status', '')
		userprofile.user_type = 'staff'
		userprofile.save()
		try:
			userprofile.save()
		except:
			user.delete()
			response.update({'error':True})
			return render(request, 'userprofile/add_employee.html', response)

		# initialize employee object
		employee = Employee()
		employee.userprofile = userprofile
		employee.employee_type = request.POST.get('employee_type', '')
		employee.date_joined = datetime.datetime.strptime(request.POST.get('date_joined', ''), '%m/%d/%Y')

		try:
			employee.save()
		except:
			user.delete()
			response.update({'error':True})
			return render(request, 'userprofile/add_employee.html', response)

		response.update({'success':True})

	return render(request, 'userprofile/add_employee.html', response)

@login_required
def employees_list(request):
	response = {}

	employees = Employee.objects.select_related('userprofile__user').all()

	page = request.GET.get('page', '1')
	employees = MyPaginator(employees, page)

	response.update({'employees':employees})
	return render(request, 'userprofile/employees_list.html', response)


