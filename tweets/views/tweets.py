from rest_framework import generics, status
from rest_framework.response import Response

from tweets.models import TweetModel
from tweets.serializers import TweetSerializer


class TweetView(generics.CreateAPIView):
    serializer_class = TweetSerializer
    queryset = TweetModel.objects.all()

    def perform_create(self, serializer):
        # Assume request.user is the owner
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
