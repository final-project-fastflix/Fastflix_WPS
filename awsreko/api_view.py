import boto3
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer


class FaceRecommend(APIView):
    """

        사진을 보내면 얼굴 표정을 인식하여 영화 추천을 하는 API입니다.

        ---

            Header에
                Authorization : Token 토큰값

            Body에
                image : 이미지.png 또는 이미지.jpeg
            를 보내주세요

            리턴값 :
                {
                    "response": {
                        "id": 영화의 ID
                        "name": 영화 이름
                        "horizontal_image_path": 영화 가로 이미지 path
                        "vertical_image": 영화 세로 이미지 path
                        "ios_main_image": IOS에서 사용하는 이미지
                    }
               }


    """
    def post(self, request):
        imageFile = request.data['image']
        client = boto3.client('rekognition', region_name='ap-northeast-2')

        response = client.detect_faces(Image={'Bytes': imageFile.read()}, Attributes=['ALL'])
        emotion = response['FaceDetails'][0]['Emotions']
        emotion_type = sorted(emotion, key=lambda typ: typ['Confidence'], reverse=True)[0]['Type']

        if emotion_type == 'SAD':
            queryset = Movie.objects.get(name='지금 만나러 갑니다')

        else:
            genre_list = {
                # 'SAD': '지금 만나러 갑니다',
                'SURPRISED': '호러',
                'ANGRY': '액션',
                'CONFUSED': 'SF',
                'CALM': '로맨틱',
                'DISGUSTED': '피투성이 호러 영화',
                'HAPPY': '코미디',
            }

            genre = genre_list[emotion_type]
            queryset = Movie.objects.filter(genre__name__icontains=genre).order_by("?").first()

        serializer = MovieSerializer(instance=queryset, many=False)

        return Response({'response': serializer.data}, status=status.HTTP_200_OK)
