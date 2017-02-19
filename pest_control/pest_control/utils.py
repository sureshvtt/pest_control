# Util functions for Pest Control APP

from django.db.models import Max

from customer.models import ContractInvoice

def generate_bill(contract):
	if ContractInvoice.objects.all().exists():
		invoice_no = ContractInvoice.objects.all().aggregate(Max('invoice_no'))['invoice_no__max'] + 1
	else:
		invoice_no = 1

	invoice = ContractInvoice.objects.create(
					customer=contract.customer,
					contract=contract,
					invoice_no=invoice_no,
					invoice_date=contract.date,
					bill_amount=contract.net_contract_amount,
					balance_amount=contract.net_contract_amount
				)
	return True


