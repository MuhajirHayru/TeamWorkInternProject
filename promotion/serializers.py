# promotion/serializers.py
from urllib import request
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import post, Media, Event, product, News, JobAnnouncement

class MediaSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = Media
        fields = ['id', 'file', 'title', 'media_type']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if instance.file and request:
            rep['file'] = request.build_absolute_uri(instance.file.url)
        return rep

# promotion/serializers.py
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnnouncement
        fields = '__all__'
class PostSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = post
        fields = ['id', 'post_title', 'post_caption', 'media', 'content_object']

    def get_content_object(self, obj):
        if isinstance(obj.content_object, Event):
            return EventSerializer(obj.content_object).data
        if isinstance(obj.content_object, product):
            return ProductSerializer(obj.content_object).data
        if isinstance(obj.content_object, News):
            return NewsSerializer(obj.content_object).data
        if isinstance(obj.content_object, JobAnnouncement):
            return JobSerializer(obj.content_object).data
        return None



class PostCreateSerializer(serializers.Serializer):
    post_title = serializers.CharField()
    post_caption = serializers.CharField()
    time_limit = serializers.IntegerField()
    content_model = serializers.ChoiceField(choices=['event', 'product', 'news', 'job'])
    content_data = serializers.DictField()
    media = MediaSerializer(many=True, required=False)

    def create(self, validated_data):
        model_map = {
            'event': EventSerializer,
            'product': ProductSerializer,
            'news': NewsSerializer,
            'job': JobSerializer,
        }
        serializer_class = model_map[validated_data['content_model']]
        content_serializer = serializer_class(data=validated_data['content_data'])
        content_serializer.is_valid(raise_exception=True)
        content_obj = content_serializer.save()

        content_type = ContentType.objects.get_for_model(content_obj)
        default_user, _ = User.objects.get_or_create(username="it_officer")

        post_obj = post.objects.create(
            user=default_user,
            post_title=validated_data['post_title'],
            post_caption=validated_data['post_caption'],
            time_limit=validated_data['time_limit'],
            content_type=content_type,
            object_id=content_obj.id,
            status='pending'
        )

        for i, media_data in enumerate(validated_data.get('media', [])):
            file = request.FILES.get(f'media[{i}].file')
            media_obj = Media.objects.create(
                file=file,
                title=media_data.get('title'),
                media_type=media_data.get('media_type'),
            )
            post_obj.media.add(media_obj)

        return post_obj
