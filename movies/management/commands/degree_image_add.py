from django.core.management.base import BaseCommand

from movies.models import Movie


# class Command(BaseCommand):
#     help = 'degree image add'
#
#     def handle(self, *args, **options):
#         object_list = Movie.objects.all().order_by('id')
#         for object in object_list:
#             if '12' in object.degree.name:
#                 object.degree_path = 'http://52.78.134.79/12age.png'
#                 continue
#             if '15' in object.degree.name:
#                 object.degree_path = 'http://52.78.134.79/15age.png'
#                 continue
#             if '청소년' in object.degree.name:
#                 object.degree_path = 'http://52.78.134.79/adultage.png'
#                 continue
#             if '모든' in object.degree.name:
#                 object.degree_path = 'http://52.78.134.79/allage.png'
#                 continue
