from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, help_text='The unique identifier of the post')
    title = serializers.CharField(
        max_length=100,
        help_text='The title of the post',
        label='Title',
        required=True
    )
    content = serializers.CharField(
        style={'base_template': 'textarea.html'},
        help_text='The content of the post',
        label='Content',
        required=True
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content','author','date_posted']

    def validate_title(self, value):
        existing_title = Post.objects.filter(title=value).exists()
        if existing_title:
            raise serializers.ValidationError("Title already exists")
        return value

    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Content is too short")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        post = Post.objects.create(author=user, **validated_data)
        return post