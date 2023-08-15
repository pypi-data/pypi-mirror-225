from django.urls import path
from . import views

urlpatterns = [
	path('dash/', views.AttendDash, name="attend-dash"),
	path('import/list/', views.AttendList, name="attend-list"),
	path('day/list/<int:day>/<int:month>/<int:year>/', views.AttendDayList, name="attend-day-list"),
	path('import/<int:day>/<int:month>/<int:year>/', views.AttendImport, name="attend-import"),
	path('unit/list/<str:pk>/', views.AttendUnitList, name="attend-unit-list"),
	path('unit/day/<str:pk>/<str:day>/', views.AttendUnitDayEmp, name="attend-unit-day"),
	path('unit/emp/<str:pk>/<str:hashid>', views.AttendUnitEmpDay, name="attend-unit-emp"),
	path('process/am/<str:hashid>/', views.AttendProcessAM, name="attend-process-am"),
	path('process/pm/<str:hashid>/', views.AttendProcessPM, name="attend-process-pm"),
	path('process/emp/<str:pk>/<str:hashid>/<str:day>/', views.AttendUnitEmpProcess, name="attend-process-emp"),
	path('emp/update/<str:pk>/<str:hashid>/<str:day>/<str:pk2>/', views.AttendUnitEmpUpdate, name="attend-emp-update"),
	path('present/yes/<str:pk>/<str:hashid>/', views.AttendPresYes, name="attend-present-yes"),
	path('present/no/<str:pk>/<str:hashid>/', views.AttendPresNo, name="attend-present-no"),

	# path('dg/list/<str:hashid>/', views.AttendanceDGList, name="attendance-dg-list"),
	# path('dg/day/<str:dgid>/<str:day>/', views.AttendanceDGDayEmp, name="attendance-dg-day"),
	# path('dg/emp/<str:dgid>/<str:hashid>', views.AttendanceDGEmpDay, name="attendance-dg-emp"),

	path('upload/<str:unitid>/<str:year>/<str:month>/', views.AttendUpload, name="attend-upload"),
	path('confirm/<str:pk>/', views.AttendConfirm, name="attend-confirm"),
	path('cancel/<str:pk>/', views.AttendCancel, name="attend-cancel"),
	path('final/confirm/<str:pk>/', views.AttendFinalConfirm, name="attend-final-confirm"),
	path('view/pdf/<str:pk>/', views.AttendPDF, name="attend-pdf"),
	path('print/<str:pk>/<str:year>/<str:month>/', views.AttendPrint, name="attend-print"),

	path('custom/dash/', views.AttendanceSetDash, name="attend-custom-dash"),
	path('custom/year/<str:pk>/', views.AttendanceSetYear, name="attend-custom-year"),
	path('custom/month/<str:pk>/', views.AttendanceSetMonth, name="attend-custom-month"),
	path('custom/status/add/', views.AttendanceStatusAdd, name="attend-custom-status-add"),
	path('custom/status/update/<str:pk>/', views.AttendanceStatusUpdate, name="attend-custom-status-update"),
	path('custom/holiday/list/', views.HolidayList, name="attend-custom-holiday-list"),
	path('custom/holiday/add/', views.HolidayAdd, name="attend-custom-holiday-add"),
	path('custom/holiday/update/<str:pk>/', views.HolidayUpdate, name="attend-custom-holiday-update"),
	path('custom/holiday/delete/<str:pk>/', views.HolidayDelete, name="attend-custom-holiday-delete"),
	path('r/dash/', views.RAttDash, name="r-att-dash"),
	path('r/unit/<str:pk>/<str:year>/<str:month>/', views.RAttUnitList, name="r-att-unit-list"),
	path('r/emp/search/', views.RAttEmpSearch, name="r-att-emp-search"),
	path('r/emp/<str:hashid>/dash/', views.RAttEmpDash, name="r-att-emp-dash"),
	path('r/year/licfal/', views.RLicFalYear, name="r-att-fal-year"),
	
	path('u/r/unit/dash/', views.uRAttUnitDash, name="ur-att-unit-dash"),
	path('u/r/unit/emp/search/', views.uRAttUnitEmpSearch, name="ur-att-unit-emp-search"),
	path('u/r/unit/emp/<str:pk>/<str:hashid>/dash/<str:page>/', views.uRAttUnitEmpDash, name="ur-att-unit-emp-dash"),

	path('r/print/emp/gen/<str:hashid>/', views.PrintRAttEmpGeral, name="print-r-att-emp-gen"),
	path('r/print/emp/year/<str:hashid>/<int:year>/', views.PrintRAttEmpYear, name="print-r-att-emp-gen-y"),
	path('r/print/emp/month/<str:hashid>/<int:year>/<int:month>/', views.PrintRAttEmpMonth, name="print-r-att-emp-gen-m"),
	path('r/print/licfal/<str:year>/', views.PrintLicFal, name="print-r-licfal"),
]