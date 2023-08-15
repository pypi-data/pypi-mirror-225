from django.urls import path
from . import views

urlpatterns = [
	path('emp/leave/', views.APIEmpLeave.as_view()),
	path('emp/leave/type/', views.APIEmpLeaveType.as_view()),
	path('emp/leave/type/2/<int:year>/', views.APIEmpLeaveType2.as_view()),
	path('emp/leave/type/2/<int:year>/<int:month>/', views.APIEmpLeaveType3.as_view()),
	path('emp/leave/type/unit/<int:unit>/', views.APIEmpLeaveUnit.as_view()),
	path('emp/leave/type/month/<int:month>/', views.APIEmpLeaveMonth.as_view()),
	path('emp/leave/type/tri/<int:tri>/', views.APIEmpLeaveTri.as_view()),
	path('emp/leave/type/year-unit/<int:year>/<int:unit>/', views.APIEmpLeaveYearUnit.as_view()),
	path('emp/leave/type/year-month/<int:year>/<int:month>/', views.APIEmpLeaveYearMonth.as_view()),
	path('emp/leave/type/year-tri/<int:year>/<int:tri>/', views.APIEmpLeaveYearTri.as_view()),
	path('emp/leave/type/month-unit/<int:month>/<int:unit>/', views.APIEmpLeaveMonthUnit.as_view()),
	path('emp/leave/type/year-month-unit/<int:year>/<int:month>/<int:unit>/', views.APIEmpLeaveYearMonthUnit.as_view()),
	path('emp/leave/type/year-tri-unit/<int:year>/<int:tri>/<int:unit>/', views.APIEmpLeaveYearTriUnit.as_view()),
]