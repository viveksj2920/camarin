from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from posts.models import Post
from .moderation import moderate_text
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        content = request.data.get('content', '')
        is_flagged, reason = moderate_text(content)

        comment = Comment.objects.create(
            user=request.user,
            post=Post.objects.get(id=post_id),
            content=content,
            is_flagged=is_flagged,
            flagged_reason=reason
        )

        message = "Comment submitted successfully."
        if is_flagged:
            send_mail(
                subject="⚠️ Your comment was flagged",
                message=f"Your comment on post '{comment.post.title}' was flagged.\nReason: {reason}",
                from_email=None,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

        serializer = self.get_serializer(comment)
        return Response({
            "message": message,
            "comment": serializer.data
        }, status=status.HTTP_201_CREATED)


class FlaggedCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user, is_flagged=True)