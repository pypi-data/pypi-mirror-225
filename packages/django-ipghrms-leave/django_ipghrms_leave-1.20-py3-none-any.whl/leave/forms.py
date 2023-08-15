from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Button, HTML
from django.db.models import Q
from django.contrib.auth.models import User
from leave.models import Leave, LeaveDE, LeaveDelegate, LeaveHR, LeaveUnit, LeaveDep, LeavePeriod
from django_summernote.widgets import SummernoteWidget
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
	input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

def validate_time_range(value):
    now = datetime.datetime.now().time()
    if now >= datetime.time(18, 0, 0) or now <= datetime.time(6, 0, 0):
        raise ValidationError('Input is blocked between 18:00 and 06:00')

class LeaveForm(forms.ModelForm):
	comments = forms.CharField(label="Komentariu Seluk", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	
	class Meta:
		model = Leave
		fields = [ 'description', 'leave_type','start_date','end_date', 'comments', 'file', 'start_time_status', 'end_time_status' ]
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['description'].required = True
		self.fields['start_date'].required = True
		self.fields['end_date'].required = True
		self.fields['start_time_status'].required = True
		self.fields['end_time_status'].required = True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('description', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('leave_type', css_class='form-group col-md-6 mb-0'),
                Column('file', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('start_date', css_class='form-group col-md-3 mb-0'),
                Column('end_date', css_class='form-group col-md-3 mb-0'),
                Column('start_time_status', css_class='form-group col-md-3 mb-0'),
				Column('end_time_status', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('comments', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

		
class HRLeaveCommentForm(forms.ModelForm):
	comment = forms.CharField(label="Measuring", required=False, widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '300px'}}))
	
	class Meta:
		model = Leave
		fields = ['comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['comment'].label = 'Komentario'
		self.fields['comment'].required = True
		self.helper.layout = Layout(
			Row(
				Column('comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class HRLeaveForm(forms.ModelForm):
	date = forms.DateField(label='Data Aplika', widget=DateInput(), required=False)
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	class Meta:
		model = Leave
		fields = ['description', 'leave_type','date','start_date','end_date', 'days', 'file']
		widgets = {
            "start_date": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "min": timezone.now().date()},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['description'].required = True
		self.fields['days'].required = True
		self.fields['date'].required = True
		self.fields['start_date'].required = True
		self.fields['end_date'].required = True
		self.helper.layout = Layout(
			Row(
				Column('description', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('leave_type', css_class='form-group col-md-5 mb-0'),
                Column('date', css_class='form-group col-md-5 mb-0'),
                Column('days', css_class='form-group col-md-2 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('end_date', css_class='form-group col-md-4 mb-0'),
                Column('file', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class HRLeaveFormSpecial(forms.ModelForm):
	date = forms.DateField(label='Data Aplika', widget=DateInput(), required=False)
	start_date = forms.DateField(label='Data Hahu', widget=DateInput(), required=False)
	end_date = forms.DateField(label='Data Remata', widget=DateInput(), required=False)
	start_time = forms.TimeField(widget=TimeInput)
	end_time = forms.TimeField(widget=TimeInput)
	class Meta:
		model = Leave
		fields = ['description', 'leave_type','date','start_date','end_date', 'file', 'start_time', 'end_time']
		widgets = {
            "start_date": DateInput(
                attrs={"type": "datetime-local", "class": "form-control", "min": timezone.now().date()},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_date": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['description'].required = True
		self.fields['date'].required = True
		self.fields['start_date'].required = True
		self.fields['end_date'].required = True
		self.helper.layout = Layout(
			Row(
				Column('description', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('leave_type', css_class='form-group col-md-6 mb-0'),
                Column('date', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('start_date', css_class='form-group col-md-3 mb-0'),
                Column('end_date', css_class='form-group col-md-3 mb-0'),
				Column('start_time', css_class='form-group col-md-3 mb-0'),
                Column('end_time', css_class='form-group col-md-3 mb-0'),
				css_class='form-row'
			),
			Row(
                Column('file', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class HRPeriodForm(forms.ModelForm):
	class Meta:
		model = LeavePeriod
		fields = ['start_year','end_year', 'balance_carry']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['start_year'].required=True
		self.fields['end_year'].required=True
		self.helper.form_method = 'post'
		self.fields['balance_carry'].label = 'Balance Carry Forward (Opsional)'
		self.helper.layout = Layout(
			Row(
                Column('start_year', css_class='form-group col-md-4 mb-0'),
				Column('end_year', css_class='form-group col-md-4 mb-0'),
				Column('balance_carry', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveDelegateForm1(forms.ModelForm):
	class Meta:
		model = LeaveDelegate
		fields = ['employee']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('employee', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveDelegateForm2(forms.ModelForm):
	class Meta:
		model = LeaveDelegate
		fields = ['obs','reason']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('obs', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveUnitForm(forms.ModelForm):
	class Meta:
		model = LeaveUnit
		fields = ['obs','reason']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('obs', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

# work: DEP
class LeaveDepForm(forms.ModelForm):
	class Meta:
		model = LeaveDep
		fields = ['obs','reason']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['obs'].required = True
		self.helper.layout = Layout(
			Row(
				Column('obs', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveHRForm(forms.ModelForm):
	class Meta:
		model = LeaveHR
		fields = ['obs','reason']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('obs', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveDEForm(forms.ModelForm):
	class Meta:
		model = LeaveDE
		fields = ['obs','reason']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['obs'].required=True
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('obs', css_class='form-group col-md-3 mb-0'),
				Column('reason', css_class='form-group col-md-9 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveCancelForm(forms.ModelForm):
	class Meta:
		model = Leave
		fields = ['cancel_comment']
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.fields['cancel_comment'].required=True
		self.fields['cancel_comment'].label="Razaun Kansela"
		self.helper.layout = Layout(
			Row(
				Column('cancel_comment', css_class='form-group col-md-12 mb-0'),
				css_class='form-row'
			),
			HTML(""" <button class="btn btn-primary" type="submit" title="Rai">Rai <i class="fa fa-save"></i></button> """)
		)

class LeaveFilterForm(forms.Form):
    tinan = forms.ChoiceField(choices=[(0, 'Tinan...')])
    tri = forms.ChoiceField(choices=[(0, 'Trimestral...')])
    fulkan = forms.ChoiceField(choices=[(0, 'Fulan...')])
    unit = forms.ChoiceField(choices=[(0, 'Divizaun...')])