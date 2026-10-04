from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationView(APIView):

    def get(self, request):
        notification = cache.get(f"notification:{request.user.id}")

        if notification:
            cache.delete(f"notification:{request.user.id}")

        return Response(notification)
