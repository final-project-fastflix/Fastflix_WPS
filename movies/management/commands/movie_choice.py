import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User, SubUser, LikeDisLikeMarked
from movies.models import Movie


class Command(BaseCommand):
    help = 'preview_video_file'

    def handle(self, *args, **options):

        user_id_list = User.objects.values('id')
        id_list = []
        for user_id in user_id_list:
            id_list.append(user_id['id'])

        movie_name_list = [
            '괴물', '아이언맨2', '가디언즈 오브 갤럭시', '업', '핸콕',
            '노트북', '봄날은 간다', '매그놀리아', 'SPF-18', '투모로우',
            '죠스', '사바하', '그해 여름', '오 마이 그랜파', '성질 죽이기',
            '잭애스', '예스맨', '세븐틴 어게인', '행오버 3', '행오버',
            '피터 팬', '바바둑', '플립', '큐브', '마더!',
            '퍼펙션', '시크릿 옵세션', '샤이닝', '위자', '침묵',
            '잠복근무', '의뢰인', '나의 마더', '체인지 업', '빅 히어로',
            '은혼', '라푼젤', '죠스', '샤이닝', '직쏘',
            '인시디어스 3', '무서운 영화4', '프리스트', '침묵', '잠복근무',
            '의뢰인', '나의 마더', '체인지 업', ' 픽셀', '맨 인 블랙',
            '클로버필드 패러독스', '고스트 워', '스파이더맨', '시월애', '컨트롤러',
            '반드시 잡는다', '쎄븐', '7월 22일', '다빈치 코드', '그래비티',
        ]

        for user_id in id_list:
            user = User.objects.get(id=user_id)
            # random_movie_list = Movie.objects.exclude(name__in=movie_name_list).order_by("?")[:25]
            # sum_movie = movie_list.union(random_movie_list)

            sub_user_list = SubUser.objects.filter(parent_user=user)

            for sub_user in sub_user_list:
                random_movie_list = random.sample(movie_name_list, 5)

                movie_list = Movie.objects.filter(name__in=random_movie_list)
                for movie in movie_list:
                    obj, created = LikeDisLikeMarked.objects.update_or_create(
                        movie=movie,
                        sub_user=sub_user,
                        defaults={'movie': movie,
                                  'sub_user': sub_user,
                                  'updated': timezone.now(),
                                  })
                    if created:
                        obj.marked = True
                        obj.like_or_dislike = 1
                        obj.save()

            # for sub_user in sub_user_list:
