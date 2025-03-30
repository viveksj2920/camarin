from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'is_flagged', 'flagged_reason', 'created_at']
        read_only_fields = ['user', 'is_flagged', 'flagged_reason', 'created_at']
