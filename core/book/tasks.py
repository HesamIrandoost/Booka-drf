from celery import shared_task
from django.core.cache import cache


@shared_task
def send_review_notification(user_id, book_title):

    message = {
        "type": "review_created",
        "message": f"Review created for '{book_title}'",
    }

    cache.set(
        f"notification:{user_id}",
        message,
        timeout=60,
    )

    return message
