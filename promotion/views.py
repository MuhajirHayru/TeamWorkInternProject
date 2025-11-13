# My name is muhajir hayru i updated the post image and i did the post inside t
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import post, Media
from .serializers import PostCreateSerializer, PostSerializer
import json
# Generic create view (unchanged)
class createGenerics(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
#and also i teste the create test and in which i can test by the way i testeed in the postman and it is working correctly
class CreatePostView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        data = request.data.copy()

        # Parse content_data
        raw_content = data.get('content_data')
        if isinstance(raw_content, str):
            try:
                data['content_data'] = json.loads(raw_content)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON in content_data'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostCreateSerializer(data=data)
        if serializer.is_valid():
            post_obj = serializer.save()

            # ✅ Handle uploaded media files
            files = request.FILES.getlist('media')
            for file in files:
                media_obj = Media.objects.create(file=file, media_type='image')
                post_obj.media.add(media_obj)

            return Response({'message': 'Post created', 'post_id': post_obj.id}, status=status.HTTP_201_CREATED)

        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ApprovePostView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        post_obj = get_object_or_404(post, pk=pk)
        post_obj.status = 'approved'
        post_obj.save()
        return Response({'message': 'Post approved'})

# Post viewset (unchanged)
class PostViewSet(viewsets.ModelViewSet):
    queryset = post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs