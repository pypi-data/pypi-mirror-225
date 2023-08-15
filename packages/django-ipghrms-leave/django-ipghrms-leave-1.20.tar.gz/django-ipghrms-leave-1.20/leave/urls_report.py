from django.urls import path
from . import views

urlpatterns = [
	### Staff
	path('dash/', views.hrLeaveReportDash, name="hr-leave-r-dash"),
	path('type/<int:pk>/<int:year>/list/', views.hrLeaveReportLeaveTypeList, name="hr-leave-r-list-type"),
	path('type/<int:year>/list-all/', views.hrLeaveReportLeaveTypeListAll, name="hr-leave-r-list-all"),
	path('type/month/<str:date>/list/', views.hrLeaveReportLeaveMonthTypeList, name="hr-leave-r-list-day"),
	# YEARS
	path('type/year/<int:pk>/<int:year>/', views.hrReportLeaveYear, name="hr-report-year"),
	path('type/year-all/<int:year>/', views.hrReportLeaveYearAll, name="hr-report-year-all"),
	# UNITS
	path('type/unit/<int:pk>/<int:pk2>/', views.hrReportLeaveUnit, name="hr-report-unit"),
	path('type/unit-all/<int:pk>/', views.hrReportLeaveUnitAll, name="hr-report-unit-all"),
	# TRI
	path('type/tri/<int:pk>/<int:pk2>/', views.hrReportLeaveTri, name="hr-report-tri"),
	path('type/tri-all/', views.hrReportLeaveTriAll, name="hr-report-tri-all"),
	# MONTH 
	path('type/month/<int:pk>/<int:month>/', views.hrReportLeaveMonth, name="hr-report-month"),
	path('type/month-all/<int:month>/', views.hrReportLeaveMonthAll, name="hr-report-month-all"),
	# YEAR UNIT 
	path('type/year-unit/<int:pk>/<int:pk2>/<int:year>/', views.hrReportLeaveYearUnit, name="hr-report-year-unit"),
	path('type/year-unit-all/<int:pk>/<int:year>/', views.hrReportLeaveYearUnitAll, name="hr-report-year-unit-all"),
	# YEAR MONTH 
	path('type/year-month/<int:pk>/<int:year>/<int:month>/', views.hrReportLeaveMonth, name="hr-report-year-month"),
	path('type/year-month-all/<int:year>/<int:month>/', views.hrReportLeaveMonthAll, name="hr-report-year-month-all"),
	# MONTH UNIT 
	path('type/month-unit/<int:pk>/<int:month>/<int:unit>/', views.hrReportLeaveMonthUnit, name="hr-report-month-unit"),
	path('type/month-unit-all/<int:month>/<int:unit>/', views.hrReportLeaveMonthUnitAll, name="hr-report-month-unit-all"),
	# YEAR TRI 
	path('type/year-tri/<int:pk>/<int:year>/<int:gtri>/', views.hrReportLeaveYearTri, name="hr-report-year-tri"),
	path('type/year-tri-all/<int:year>/', views.hrReportLeaveYearTriAll, name="hr-report-year-tri-all"),
	# YEAR MONTH UNIT 
	path('type/year-month-unit/<int:pk>/<int:year>/<int:month>/<int:unit>/', views.hrReportLeaveYearMonthUnit, name="hr-report-year-month-unit"),
	path('type/year-month-unit-all/<int:year>/<int:month>/<int:unit>/', views.hrReportLeaveYearMonthUnitAll, name="hr-report-year-month-unit-all"),
	# YEAR TRI UNIT 
	path('type/year-tri-unit/<int:pk>/<int:year>/<int:gtri>/<int:unit>/', views.hrReportLeaveYearTriUnit, name="hr-report-year-tri-unit"),
	path('type/year-tri-unit-all/<int:year>/<int:unit>/', views.hrReportLeaveYearTriUnitAll, name="hr-report-year-tri-unit-all"),
]