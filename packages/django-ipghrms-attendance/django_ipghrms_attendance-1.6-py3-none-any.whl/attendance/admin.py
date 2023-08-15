from django.contrib import admin
from .models import *

admin.site.register(Year)
admin.site.register(Month)
admin.site.register(Attendance)
admin.site.register(AttendanceUnit)
admin.site.register(AttendanceTotal)
admin.site.register(AttendanceStatus)