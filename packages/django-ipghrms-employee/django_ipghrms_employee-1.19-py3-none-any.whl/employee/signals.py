from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, FIDNumber, LIDNumber, IIDNumber, ContactInfo, LocationTL,\
    LocationInter, AddressTL, Photo, DriverLicence, CurEmpPosition, CurEmpDivision

@receiver(post_save, sender=Employee)
def create_employee(sender, instance, created, **kwargs):
	
	if created:
		FIDNumber.objects.create(id=instance.id, employee=instance)
		LIDNumber.objects.create(id=instance.id, employee=instance)
		IIDNumber.objects.create(id=instance.id, employee=instance)
		LocationTL.objects.create(id=instance.id, employee=instance)
		LocationInter.objects.create(id=instance.id, employee=instance)
		ContactInfo.objects.create(id=instance.id, employee=instance)
		AddressTL.objects.create(id=instance.id, employee=instance)
		Photo.objects.create(id=instance.id, employee=instance)
		DriverLicence.objects.create(id=instance.id, employee=instance)
		CurEmpPosition.objects.create(id=instance.id, employee=instance)
		CurEmpDivision.objects.create(id=instance.id, employee=instance)