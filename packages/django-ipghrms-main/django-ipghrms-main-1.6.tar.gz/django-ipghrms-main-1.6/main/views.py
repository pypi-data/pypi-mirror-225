from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from contract.models import Contract, EmpSalary
from employee.models import AddressTL, ContactInfo, CurEmpDivision, CurEmpPosition, DriverLicence,\
	EmpDependency, FIDNumber, FormalEducation, IIDNumber, LIDNumber, LocationInter, LocationTL,\
	NonFormalEducation, Photo, WorkExperience
from recruitment2.models import Plan, Painel
from settings_app.user_utils import c_staff, c_dep, c_unit, c_user_de, c_user_deputy
from users.context_processors import user_group
@login_required
def home(request):
	group = user_group(request)
	c_emp, _ = c_unit(request.user)
	recplan = Plan.objects.filter(is_active=True).first()
	recplanall = Plan.objects.filter(is_active=True)
	painel_check = []
	painels = Painel.objects.filter(plan=recplan, employee=c_emp).select_related('employee', 'plan')
	for obj in recplanall:
		pc = Painel.objects.filter(plan=obj, employee=c_emp).select_related('employee', 'plan')
		if pc:
			for i in pc:
				painel_check.append(i)
	if group == 'staff':
		objects = c_staff(request.user)
		fidnum = FIDNumber.objects.filter(employee=objects).first()
		lidnum = LIDNumber.objects.filter(employee=objects).first()
		iidnum = IIDNumber.objects.filter(employee=objects).first()
		continfo = ContactInfo.objects.filter(employee=objects).first()
		loctl = LocationTL.objects.filter(employee=objects).first()
		addtl = AddressTL.objects.filter(employee=objects).first()
		locinter = LocationInter.objects.filter(employee=objects).first()
		img = Photo.objects.filter(employee=objects).first()
		driver = DriverLicence.objects.filter(employee=objects).first()
		empcontract = Contract.objects.filter(employee=objects, is_active=True).last()
		empsalary = EmpSalary.objects.filter(contract=empcontract).last()
		emppos = CurEmpPosition.objects.filter(employee=objects).first()
		empdiv = CurEmpDivision.objects.filter(employee=objects).first()
		empdepends = EmpDependency.objects.filter(employee=objects).all()
		formaledus = FormalEducation.objects.filter(employee=objects).all()
		nonformaledus = NonFormalEducation.objects.filter(employee=objects).all()
		workexps = WorkExperience.objects.filter(employee=objects).all()
		
		painels = Painel.objects.filter(plan=recplan, employee=objects).all()
		painel_check = Painel.objects.filter(plan=recplan, employee=objects).first()
		context = {
			'group': group, 'objects': objects, 'fidnum': fidnum, 'lidnum': lidnum, 'iidnum': iidnum,
			'continfo': continfo, 'loctl':loctl, 'addtl': addtl, 'locinter': locinter, 'img': img,
			'formaledus': formaledus, 'nonformaleds': nonformaledus, 'workexps': workexps,
			'empdepends': empdepends, 'empcontract': empcontract, 'empsalary': empsalary,
			'driver': driver, 'emppos': emppos, 'empdiv': empdiv,
			'recplan': recplan, 'painels': painels, 'painel_check': painel_check,
			'title': 'Hu nia Perfil', 'legend': 'Hu nia Perfil'
		}
		return render(request, 'home/home_staff.html', context)
	elif group == 'dep':
		c_emp, _ = c_dep(request.user)
		painel_check = []
		painels = Painel.objects.filter(plan=recplan, employee=c_emp).all()
		for obj in recplanall:
			pc = Painel.objects.filter(plan=obj, employee=c_emp)
			if pc:
				for i in pc:
					painel_check.append(i)
		context = {
			'group': group, 'recplan': recplan, 'painels': painels, 'painel_check': painel_check,
			'title': 'Painel HRMS', 'legend': 'Painel HRMS'
		}
		return render(request, 'home/home_dep.html', context)
	elif group == 'unit':
		c_emp, _ = c_unit(request.user)
		painel_check = []
		painels = Painel.objects.filter(plan=recplan, employee=c_emp).all()
		for obj in recplanall:
			pc = Painel.objects.filter(plan=obj, employee=c_emp)
			if pc:
				for i in pc:
					painel_check.append(i)
		context = {
			'group': group, 'recplan': recplan, 'painels': painels, 'painel_check': painel_check,
			'title': 'Painel HRMS', 'legend': 'Painel HRMS'
		}
		return render(request, 'home/home_unit.html', context)
	else: 
		context = { 'group': group, 'title': 'Painel HRMS', 'legend': 'Painel HRMS', 'painel_check':painel_check }
		return render(request, 'home/home.html', context)
	
def handle_404(request, exception):
    template_name = "home/404.html"
    return render(request, template_name, status=404)

def handle_500(request, exception):
    template_name = "home/500.html"
    return render(request, template_name, status=404)

