from celery import shared_task
from celery.utils.log import get_task_logger
from .models import *
from authMiddleware.models import *
from django.db import transaction

from .serializers import *

logger = get_task_logger(__name__)


@shared_task
def clap_post(user_email, post_uuid, count):
    with transaction.atomic():
        try:
            post = Post.objects.get(id=post_uuid)
            post.claps = post.claps + count

            clap, created = Clap.objects.get_or_create(
                user_id=user_email, post_id=post_uuid
            )

            if created:
                clap.claps = count
            else:
                claps = int(clap.claps)
                clap.claps = claps + count

            clap.save()
            post.save()

            logger.info(
                f"Saved {count} clap(s) for user {user_email} on post {post_uuid}"
            )

            return True

        except Exception as e:
            return False
