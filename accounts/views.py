from openpyxl import load_workbook

from accounts.models import ProfileImage, ProfileImageCategory
from movies.models import *

def origin(request):

    wb2 = load_workbook('fast_flix.xlsx')
    ws = wb2.active

    for row in ws.values:
        if row[3] == 1:
            a = Movie.objects.get(pk=row[0])
            a.genre.add(Genre.objects.get(name='넷플릭스 오리지널'))
            a.save()


