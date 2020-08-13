from django.contrib import admin
from medstore.models import Company
from medstore.models import Medicine
from medstore.models import MedicalDetails
from medstore.models import Employee
from medstore.models import Customer
from medstore.models import Bill
from medstore.models import EmployeeSalary
from medstore.models import BillDetails
from medstore.models import CustomerRequest
from medstore.models import CompanyAccount
from medstore.models import CompanyBank
from medstore.models import EmployeeBank

admin.site.register(Company)
admin.site.register(Medicine)
admin.site.register(MedicalDetails)
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Bill)
admin.site.register(EmployeeSalary)
admin.site.register(BillDetails)
admin.site.register(CustomerRequest)
admin.site.register(CompanyAccount)
admin.site.register(CompanyBank)
admin.site.register(EmployeeBank)
