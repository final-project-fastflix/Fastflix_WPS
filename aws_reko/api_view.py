import boto3
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer


class FaceRecommend(APIView):
    def post(self, request):
        imageFile = request.data['image']
        client = boto3.client('rekognition')

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
