from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Leave, LeaveDE, LeaveDelegate, LeaveHR, LeaveUnit, LeaveDep

@receiver(post_save, sender=Leave)
def create_leave(sender, instance, created, **kwargs):
	
	if created:
		LeaveDelegate.objects.create(id=instance.id, leave=instance, hashed=instance.hashed)
		LeaveUnit.objects.create(id=instance.id, leave=instance, hashed=instance.hashed)
		LeaveDep.objects.create(id=instance.id, leave=instance, hashed=instance.hashed)
		LeaveHR.objects.create(id=instance.id, leave=instance, hashed=instance.hashed)
		LeaveDE.objects.create(id=instance.id, leave=instance, hashed=instance.hashed)