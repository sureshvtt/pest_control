from django.conf.urls import url
from django.contrib import admin

import views
import userprofile.views
import customer.views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),

	# Userprofile Dashboard views

	url(r'^check/username/availability/$', userprofile.views.check_username_availabilty, name='check-username-availabilty'),

	url(r'^dashboard/$', userprofile.views.dashboard, name='userprofile-dashboard'),
	url(r'^add/enquiry/$', userprofile.views.add_enquiry, name='add-enquiry'),
	url(r'^enquiry/report/$', userprofile.views.enquiry_report, name='enquiry-report'),
	url(r'^enquiry/(?P<enq_id>[\w|\W]+)/contract/$', userprofile.views.add_contract, name='add-contract'),
	url(r'^enquiry/(?P<enq_id>[\w|\W]+)/$', userprofile.views.edit_enquiry, name='edit-enquiry'),
	url(r'^contract/report/$', userprofile.views.contract_report, name='contract-report'),
	url(r'^contract/(?P<contract_id>[\w|\W]+)/$', userprofile.views.contract_details, name='contract-details'),
	url(r'^add/employee/$', userprofile.views.add_employee, name='add-employee'),
	url(r'^employees/list/$', userprofile.views.employees_list, name='employees-list'),
]
