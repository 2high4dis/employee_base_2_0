from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from .models import Employee


@receiver(pre_delete, sender=Employee)
def balance_subordinates(sender: Employee, instance: Employee, **kwargs):
    for entry in instance.get_children():
        entry.parent = instance.parent
        entry.save()
