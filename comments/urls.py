from django.urls import path
from .views import CommentCreateView,FlaggedCommentsView

urlpatterns = [
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(), name='create-comment'),
    path('comments/flagged/', FlaggedCommentsView.as_view(), name='flagged-comments'),

]
