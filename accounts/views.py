# from openpyxl import load_workbook

from accounts.models import ProfileImage, ProfileImageCategory
from movies.models import *


# def update_real(request):
#     querryset = Movie.objects.filter(real_running_time=0)
#     for obj in querryset:
#         target_running_time = obj.running_time
#         if '시간 ' in target_running_time:
#             target_running_time = target_running_time.split('시간 ')
#             total_minute = int(target_running_time[0]) * 60 * 60 + int(target_running_time[1][:-1])*60
#         else:
#             total_minute = int(target_running_time[:-1]) * 60
#
#         obj.real_running_time = total_minute
#         obj.save()

def update_real(request):
    Movie.objects.all().update(real_running_time=30)
