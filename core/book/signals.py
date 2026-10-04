from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Review, Author


@receiver(post_save, sender=Author)
def create_author_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        instance.slug = slugify(
            f"{instance.first_name}-{instance.last_name}-{instance.pk}"
        )
        instance.save(update_fields=["slug"])
