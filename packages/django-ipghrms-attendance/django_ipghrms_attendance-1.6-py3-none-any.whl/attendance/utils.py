
from attendance.models import Attendance
import datetime as dt
import calendar
from django.utils import timezone

def sum_times(time_list):
    total_minutes = sum(int(time.split(":")[0]) * 60 + int(time.split(":")[1]) for time in time_list)
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours:02}:{minutes:02}"

def calculate_total_hours_week(week, att):
    total_hours_week = 0.00
    tot_hours_week = []
    time_wam, time_wpm, time_string_wam,time_string_wpm = '00:00', '00:00','00:00', '00:00'
    for obj4 in att:
        if obj4.totat_am:
            time_wam = obj4.totat_am
            time_string_wam = time_wam.strftime("%H:%M")
            tot_hours_week.append(time_string_wam)
        if obj4.totat_pm:
            time_wpm = obj4.totat_pm
            time_string_wpm = time_wpm.strftime("%H:%M")
            tot_hours_week.append(time_string_wpm)
        tot_hours = sum_times(tot_hours_week)
        total_hours_week = tot_hours
    return tot_hours_week


def get_weeks(year, month):
    weeks = []
    first_day = timezone.make_aware(dt.datetime(year, month, 1))
    last_day = timezone.make_aware(dt.datetime(year, month, calendar.monthrange(year, month)[1]))
    for week in range(0, (last_day - first_day).days, 7):
        week_start = first_day + dt.timedelta(days=week)
        week_end = week_start + dt.timedelta(days=6)
        weeks.append((week_start, week_end))
    return weeks