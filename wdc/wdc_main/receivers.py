from django.core.signals import request_finished
from django.dispatch import receiver
from models import Request


@receiver(request_finished)
def update_weights(sender, **kwargs):
    """
    Update every weight in the queue.
    """
    for request in Request.objects.filter(is_taken=False):
        request.set_weight()
