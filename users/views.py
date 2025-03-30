from rest_framework import generics
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer
from .utils import email_verification_token

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        token = email_verification_token.make_token(user)
        uid = user.pk

        verification_link = f"{settings.FRONTEND_URL}/verify-email/?uid={uid}&token={token}"

        send_mail(
            subject="Verify your email address",
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


@api_view(["GET"])
def verify_email(request):
    uid = request.GET.get("uid")
    token = request.GET.get("token")

    if not uid or not token:
        return JsonResponse({"error": "Missing UID or token"}, status=400)

    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid user"}, status=400)

    if email_verification_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return JsonResponse({"message": "Email verified successfully!"})
    else:
        return JsonResponse({"error": "Invalid or expired token"}, status=400)
