from django.contrib.auth.models import User
from django.db.models import signals

from blogs.models import Blog


def create_blog(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        Blog.objects.create(user=instance)


signals.post_save.connect(
    create_blog, sender=User, weak=False, dispatch_uid="models.create_blog"
)
