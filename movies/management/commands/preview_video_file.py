from django.core.management.base import BaseCommand

from movies.models import Movie


class Command(BaseCommand):
    help = 'preview_video_file'

    def handle(self, *args, **options):
        object_list = Movie.objects.all()
        count = 0
        for obj in object_list:
            if obj.video_file is "":
                count += 1

