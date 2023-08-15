from django.db import models
from django.contrib.auth.models import User
from employee.models import Employee
from settings_app.upload_utils import upload_leave
from django.core.validators import FileExtensionValidator

class Year(models.Model):
	year = models.IntegerField(null=True, blank=True)
	
	def __str__(self):
		template = '{0.year}'
		return template.format(self)

class Month(models.Model):
	code = models.IntegerField(null=True, blank=True)
	name = models.CharField(max_length=20, null=True, blank=True)
	def __str__(self):
		template = '{0.name} '
		return template.format(self)
	
class LeavePeriod(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaveperiod', null=True)
	start_month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Fulan Hahu", related_name="start_month")
	start_year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tinan Hahu", related_name="start_year")
	start_date = models.DateField(null=True, blank=True, verbose_name="Data Hahu")
	end_date = models.DateField(null=True, blank=True, verbose_name="Data Remate")
	end_month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Fulan Remata", related_name="end_month")
	end_year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tinan Remata", related_name="end_year")
	balance_carry = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00, verbose_name="Balansu Carry Forward") 
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return f' {self.employee} - {self.start_month} - {self.start_year} - {self.end_month} - {self.end_year}'
	

class LeaveType(models.Model):
	name = models.CharField(max_length=20, null=True, blank=True, verbose_name="Naran")
	total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	start_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Balance Start")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Leave(models.Model):
	description = models.CharField(max_length=250, null=True, blank=True, verbose_name="Deskrisaun Licensa")
	comments = models.TextField(null=True, blank=True, verbose_name="Komentariu Seluk")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave')
	leave_period = models.ForeignKey(LeavePeriod, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Leave Period", related_name="leaveperiod")
	leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leave', verbose_name="Tipu Licensa")
	date = models.DateField(null=True, blank=True)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	start_time = models.TimeField(null=True, blank=True, verbose_name="Horas Hahu")
	end_time = models.TimeField(null=True, blank=True, verbose_name="Horas Remata")
	days = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Loron")
	start_time_status = models.CharField(choices=[('08:00','08:00'), ('13:00', '13:00')], max_length=15, null=True, blank=True, verbose_name="Horas Hahu Licensa")
	end_time_status = models.CharField(choices=[('12:00','12:00'), ('17:00', '17:00')], max_length=15, null=True, blank=True, verbose_name="Horas Remata Licensa")
	start_date_status = models.CharField(choices=[('Dader','Dader'), ('Lokraik', 'Lokraik')], max_length=15, null=True, blank=True, verbose_name="Horas Data Hahu")
	end_date_status = models.CharField(choices=[('Dader','Dader'), ('Lokraik', 'Lokraik')], max_length=15, null=True, blank=True, verbose_name="Horas Data Remata")
	is_active = models.BooleanField(default=True, null=True)
	is_lock = models.BooleanField(default=False, null=True)
	is_send = models.BooleanField(default=False, null=True)
	is_special = models.BooleanField(default=False, null=True, blank=True)
	is_create_by_hr = models.BooleanField(default=False, null=True, blank=True)
	is_send_to_div = models.BooleanField(default=False, null=True)
	is_delegate = models.BooleanField(default=False, null=True)
	is_update = models.BooleanField(default=False, null=True)
	dep_confirm = models.BooleanField(default=False, null=True)
	dep_send = models.BooleanField(default=False, null=True)
	dep_send_pr = models.BooleanField(default=False, null=True)
	unit_send_pr = models.BooleanField(default=False, null=True)
	unit_confirm = models.BooleanField(default=False, null=True)
	unit_send = models.BooleanField(default=False, null=True)
	vice_send_pr = models.BooleanField(default=False, null=True)
	hr_confirm = models.BooleanField(default=False, null=True)
	hr_send = models.BooleanField(default=False, null=True)
	pr_approve = models.BooleanField(default=False, null=True)
	pr_notify = models.BooleanField(default=False, null=True)
	de_approve = models.BooleanField(default=False, null=True)
	pr_send = models.BooleanField(default=False, null=True)
	is_reject = models.BooleanField(default=False, null=True)
	is_approve = models.BooleanField(default=False, null=True)
	is_finish = models.BooleanField(default=False, null=True)
	is_done = models.BooleanField(default=False, null=True)
	is_print = models.BooleanField(default=False, null=True)
	is_cancel = models.BooleanField(default=False, null=True)
	cancel_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="cancelby")
	cancel_comment = models.TextField(null=True, blank=True)
	file = models.FileField(upload_to=upload_leave, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Upload Anekso")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.employee} - {0.leave_type}'
		return template.format(self)

class LeaveDelegate(models.Model):
	leave = models.OneToOneField(Leave, on_delete=models.CASCADE, related_name='leavedelegate')
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='leavedelegate', verbose_name="Delega ba")
	obs = models.CharField(choices=[('Sim','Sim'),('Lae','Lae')], max_length=3, null=True, blank=True, verbose_name="Simu Delegasaun")
	reason = models.TextField(null=True, blank=True, verbose_name="Rajaun")
	is_confirm = models.BooleanField(default=False, null=True)
	is_confirm2 = models.BooleanField(default=False, null=True)
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.leave} - {0.employee}'
		return template.format(self)

class LeaveDep(models.Model):
	leave = models.OneToOneField(Leave, on_delete=models.CASCADE, related_name='leavedep')
	obs = models.CharField(choices=[('Sim','Sim'),('Lae','Lae')], max_length=3, null=True, blank=True, verbose_name="Aprova")
	reason = models.TextField(null=True, blank=True, verbose_name="Rajaun")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.leave} - {0.obs}'
		return template.format(self)

class LeaveUnit(models.Model):
	leave = models.OneToOneField(Leave, on_delete=models.CASCADE, related_name='leaveunit')
	obs = models.CharField(choices=[('Sim','Sim'),('Lae','Lae')], max_length=3, null=True, blank=True, verbose_name="Aprova")
	reason = models.TextField(null=True, blank=True, verbose_name="Rajaun")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.leave} - {0.obs}'
		return template.format(self)

class LeaveHR(models.Model):
	leave = models.OneToOneField(Leave, on_delete=models.CASCADE, related_name='leavehr')
	obs = models.CharField(choices=[('Sim','Sim'),('Lae','Lae')], max_length=3, null=True, blank=True, verbose_name="Certifica")
	reason = models.TextField(null=True, blank=True, verbose_name="Rajaun")
	comment = models.TextField(null=True, blank=True, verbose_name="Komentario")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.leave} - {0.obs}'
		return template.format(self)

class LeaveDE(models.Model):
	leave = models.OneToOneField(Leave, on_delete=models.CASCADE, related_name='leavede')
	obs = models.CharField(choices=[('Sim','Sim'),('Lae','Lae')], max_length=3, null=True, blank=True, verbose_name="Aprova")
	reason = models.TextField(null=True, blank=True, verbose_name="Rajaun")
	datetime = models.DateTimeField(null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	hashed = models.CharField(max_length=32, null=True)
	def __str__(self):
		template = '{0.leave} - {0.obs}'
		return template.format(self)

class LeaveCount(models.Model):
	period = models.ForeignKey(LeavePeriod, on_delete=models.CASCADE, null=True, blank=True, related_name="leaveperiodcount")
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leavecount')
	month = models.ForeignKey(Month, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Fulan", related_name="leavecountmonth")
	update_date = models.DateField(null=True, blank=True)
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tinan", related_name="leavecountyear")
	leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='leavecount', verbose_name="Tipu Licenca")
	leave_earn = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Leave Earn") #Leave Earn 1.67
	total_earn = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Total Earn") #Total Earn
	prov_total_earn = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Provision Total Earn") #Total Earn
	taken = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00, verbose_name="Taken") #Taken
	total_taken = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00, verbose_name="Total Taken") #Taken
	total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Total") #Total Taken
	balance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Balance") #Balance
	total_balance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Total Balance") 
	last_total_balance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00, verbose_name="Last Total Balance") 
	balance_month = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Balance Month") 
	balance_carry = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0.00, verbose_name="Balansu Carry Forward") # Balance Cary Forward
	total_balance_leave = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Total Balance Leave") 
	def __str__(self):
		template = '{0.employee} - {0.leave_type} - {0.month} - {0.year} - {0.total_balance}'
		return template.format(self)
