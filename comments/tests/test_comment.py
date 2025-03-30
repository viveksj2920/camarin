import pytest
from rest_framework.test import APIClient
from users.models import User
from posts.models import Post
from comments.models import Comment

# ✅ Create authenticated user
@pytest.fixture
def auth_user():
    return User.objects.create_user(username="vivek", email="vivek@test.com", password="testpass")

# ✅ API client with authentication
@pytest.fixture
def api_client(auth_user):
    client = APIClient()
    client.force_authenticate(user=auth_user)
    return client

# ✅ Create a post for commenting
@pytest.fixture
def test_post(auth_user):
    return Post.objects.create(title="Test Post", content="Sample content", author=auth_user)

# ✅ 1. Clean comment should not be flagged
@pytest.mark.django_db
def test_clean_comment(api_client, test_post, mocker):
    mocker.patch("comments.moderation.moderate_text", return_value=(False, None))
    response = api_client.post(
        f"/api/posts/{test_post.id}/comment/",
        {"content": "This is a safe comment"},
        format="json"
    )
    assert response.status_code == 201
    comment = Comment.objects.first()
    assert not comment.is_flagged
    assert comment.flagged_reason in [None, ""]

# ✅ 2. Toxic comment should be flagged
@pytest.mark.django_db
def test_flagged_comment(api_client, test_post, mocker):
    mocker.patch("comments.moderation.moderate_text", return_value=(True, "Toxic content"))
    response = api_client.post(
        f"/api/posts/{test_post.id}/comment/",
        {"content": "You are stupid"},
        format="json"
    )
    assert response.status_code == 201
    comment = Comment.objects.first()
    assert comment.is_flagged
    assert comment.flagged_reason == "Toxic content"

# ✅ 3. Empty comment should return 400
@pytest.mark.django_db
def test_empty_comment_content(api_client, test_post):
    response = api_client.post(
        f"/api/posts/{test_post.id}/comment/",
        {"content": ""},
        format="json"
    )
    assert response.status_code == 400
    assert "content" in response.data

# ✅ 4. Unauthenticated user should get 401
@pytest.mark.django_db
def test_comment_unauthenticated(test_post):
    client = APIClient()
    response = client.post(
        f"/api/posts/{test_post.id}/comment/",
        {"content": "Nice post!"},
        format="json"
    )
    assert response.status_code == 401

# ✅ 5. Commenting on non-existent post returns 404
@pytest.mark.django_db
def test_comment_nonexistent_post(api_client):
    response = api_client.post(
        "/api/posts/9999/comment/",
        {"content": "Testing invalid post"},
        format="json"
    )
    assert response.status_code == 404

# ✅ 6. Get only flagged comments for user
@pytest.mark.django_db
def test_get_flagged_comments(api_client, test_post, mocker):
    mocker.patch("comments.moderation.moderate_text", return_value=(True, "Abusive"))
    api_client.post(
        f"/api/posts/{test_post.id}/comment/",
        {"content": "Bad word here"},
        format="json"
    )
    mocker.patch("comments.moderation.moderate_text", return_value=(False, None))
    api_client.post(
        f"/api/posts/{test_post.id}/comment/",
        {"content": "All good!"},
        format="json"
    )
    response = api_client.get("/api/comments/flagged/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["flagged_reason"] == "Abusive"
