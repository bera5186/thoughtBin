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
        post = Post.objects.get(id=post_uuid)
        post.claps = post.claps + 1

        print(PostSerializer(post).data)

        

        try:
            clap = Clap.objects.get(user_id=user_email, post_id=post_uuid)
            clap.claps = clap.claps + count
            clap.save()
            post.save()
        except Clap.DoesNotExist as e:
            print(e)
            new_clap_object = Clap.objects.create(user_id=user_email, post_id=post_uuid, claps=count)
            post.save()
            new_clap_object.save(force_insert=True)
        else:
            raise Exception
        
        logger.info(f'Saved {count} clap(s) for user {user_email} on post {post_uuid}')

        return True
