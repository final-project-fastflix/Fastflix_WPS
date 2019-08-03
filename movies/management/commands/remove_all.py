from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User, SubUser, LikeDisLikeMarked
from movies.models import Movie


class Command(BaseCommand):
    help = 'preview_video_file'

    def handle(self, *args, **options):
        LikeDisLikeMarked.objects.all().delete()
