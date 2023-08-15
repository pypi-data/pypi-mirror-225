import os, hashlib
from uuid import uuid4

def getnewid(table_name):
	result = table_name.objects.last()
	if result:
		newid = result.id + 1
		hashid = hashlib.md5(str(newid).encode())
	else:
		newid = 1
		hashid = hashlib.md5(str(newid).encode())
	return newid, hashid.hexdigest()

def hash_md5(strhash):
	hashed = hashlib.md5(strhash.encode())
	return hashed.hexdigest()


def path_and_rename_photo(instance, filename):
	upload_to = 'amployee_files/{}'.format(instance.employee.id)
	field = 'photo'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)

def path_and_rename_formal(instance, filename):
	upload_to = 'amployee_files/{}'.format(instance.employee.id)
	field = 'formal'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)




def path_and_rename_nonformal(instance, filename):
	upload_to = 'amployee_files/{}'.format(instance.employee.id)
	field = 'nonformal'
	ext = filename.split('.')[-1]
	if instance.pk:
		filename = '{}_{}_{}.{}'.format(field,instance.employee.id,instance.pk,ext)
	else:
		filename = '{}.{}'.format(uuid4().hex, ext)
	return os.path.join(upload_to, filename)



from django.db.models import Q, Count
from employee.models import Employee
from contract.models import EmpPosition, EmpPlacement
from custom.models import Unit, Department

def get_employee_data():
    units = Unit.objects.all().annotate(
        num_staff=Count('curempdivision')
    )
    deps = Department.objects.all().annotate(
        num_staff=Count('curempdivision')
    )
    unitlist = [[u, u.num_staff] for u in units]
    deplist = [[d, d.num_staff] for d in deps]
    delist = EmpPosition.objects.filter(Q(position_id__in=[1, 2]), is_active=True).distinct()
    advlist = Employee.objects.filter(Q(contract__category_id__in=[3, 4]), contract__is_active=True).distinct()
    totde = delist.count()
    totadv = advlist.count()
    totunit = sum(n for _, n in unitlist)
    totdep = sum(n for _, n in deplist)
    total = totde + totunit + totadv
    return {
        'des': delist,
        'units': unitlist,
        'deps': deplist,
        'totadv': totadv,
        'totde': totde,
        'totunit': totunit,
        'totdep': totdep,
        'total': total
    }

