from .utils import get_employee_data

def employee_data(request):
    employee_data = get_employee_data()
    return {'employee_data': employee_data}
