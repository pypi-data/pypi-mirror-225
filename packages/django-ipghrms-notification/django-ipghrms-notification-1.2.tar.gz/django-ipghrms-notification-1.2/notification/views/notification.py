from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from contract.models import Contract, ContractType
from datetime import datetime, timedelta
from employee.models import Employee
from notification.utils import is_birthday_coming
from  django.http import JsonResponse
from leave.models import Leave, LeaveDep
from settings_app.user_utils import c_staff,c_unit
from django.db.models import Q
from perform.models  import Eval, Category, EvalYear, ParameterA, ParameterB, EvalPlanning, EvalPreAssessment, EvalPlanningA, EvalSelf
from leave.models import LeavePeriod, LeaveCount


# done: Notif HR
@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrNotifAllBadge(request):
    group = request.user.groups.all()[0].name
    todayYear = datetime.today().date()
    cats = Category.objects.exclude(Q(pk=1)|Q(pk=2)).order_by('name')
    employee = Employee.objects.filter(status_id=1)
    contract_list = Contract.objects.filter(is_active=True)
    birtharr = []
    d = []
    birth, cont, leave, eval, leave_end = 0,0,0,0,0
    if group == 'hr':
        for obj in employee:
            if obj.dob:
                remain_day = is_birthday_coming(obj)
                if remain_day != None:
                    birtharr.append(remain_day)
                period = LeavePeriod.objects.filter(employee=obj, is_active=True).last()
                if period:
                    if todayYear >= period.end_date:
                        leave_end += 1
        for obj in contract_list:
            if obj.end_date:
                remain_day = (datetime.now().date() - obj.end_date).days
                if remain_day >= -5 or remain_day > 0:
                    d.append(remain_day)
                    
        leave = Leave.objects.filter(
            Q(is_send=True, pr_approve=False,is_done=False)| \
            Q( Q(is_approve=True)|Q(is_reject=True, is_done=False), unit_send_pr=True, hr_confirm = False)|\
            Q(pr_notify=True,hr_confirm = False)|
            Q(pr_send=True,is_approve=True, hr_confirm = False)|
            Q(is_send_to_div=True,is_approve=True, hr_confirm=False)|
            Q(is_send_to_div=True,is_done=False, is_finish=False)|
            Q(is_approve=True, hr_confirm=False), is_cancel=False
        ).count()
    eval = Eval.objects.filter(year__is_active=True, is_finish=False).all().count()
    cont = len(d)
    birth = len(birtharr)
    dt_tot =  birth + cont + leave + eval + leave_end
    return JsonResponse({'value':dt_tot})

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def hrNotifEachBadge(request):
    group = request.user.groups.all()[0].name
    todayYear = datetime.today().date()
    cats = Category.objects.exclude(Q(pk=1)|Q(pk=2)).order_by('name')
    employee = Employee.objects.filter(status_id=1)
    contract_list = Contract.objects.filter(is_active=True)
    birtharr = []
    d = []
    birth, cont, leave, eval, leave_end = 0,0,0,0,0
    if group == 'hr':
        for obj in employee:
            if obj.dob:
                remain_day = is_birthday_coming(obj)
                if remain_day != None:
                    birtharr.append(remain_day)
            period = LeavePeriod.objects.filter(employee=obj, is_active=True).last()
            if period:    
                if todayYear >= period.end_date:
                    leave_end += 1
        for obj in contract_list:
            if obj.end_date:
                remain_day = (datetime.now().date() - obj.end_date).days
                if remain_day >= -5 or remain_day > 0:
                    d.append(remain_day)
        leave = Leave.objects.filter(
            Q(is_send=True, pr_approve=False,is_done=False)| \
            Q( Q(is_approve=True)|Q(is_reject=True, is_done=False), unit_send_pr=True, hr_confirm = False)|\
            Q(pr_notify=True,hr_confirm = False)|
            Q(pr_send=True,is_approve=True, hr_confirm = False)|
            Q(is_send_to_div=True,is_approve=True, hr_confirm=False)|
            Q(is_send_to_div=True,is_done=False, is_finish=False)|
            Q(is_approve=True, hr_confirm=False), is_cancel=False
            
        ).count()
        eval = Eval.objects.filter(year__is_active=True, is_finish=False).all().count()
    cont = len(d)
    birth = len(birtharr)
    return JsonResponse({'data1':birth, 'data2': cont, 'data3':leave, 'data4': eval, 'data5': leave_end})




@login_required
@allowed_users(allowed_roles=['admin','hr'])
def BirthdayList(request):
    objects = []
    employee = Employee.objects.filter(status_id=1).order_by('dob__day')
    for obj in employee:
        if obj.dob:
            remain_day = is_birthday_coming(obj)
            if remain_day != None:
                objects.append(remain_day)
                
    context = {
        'legend': 'Lista funsionario sei halo tinan','title': 'Lista funsionario sei halo tinan',
        'objects': objects, 'today': datetime.today().date()
    }
    return render(request, 'notification/hr/birthday.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def EndContractList(request):
    objects = []
    contract_list = Contract.objects.filter(is_active=True)
    for obj in contract_list:
        if obj.end_date:
            remain_day = (datetime.now().date() - obj.end_date).days
            if remain_day >= -5 or remain_day > 0:
                objects.append([obj, remain_day])
    context = {
        'legend': 'Lista kontrato atu mate','title': 'Lista kontrato atu mate',
        'objects': objects

    }
    return render(request, 'notification/hr/contract.html', context)

@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LeaveList(request):
    leave = Leave.objects.filter(
            Q(is_send=True, pr_approve=False,is_done=False)| \
            Q( Q(is_approve=True)|Q(is_reject=True, is_done=False), unit_send_pr=True, hr_confirm = False)| \
            Q(pr_notify=True,hr_confirm = False)|    
            Q(pr_send=True,is_approve=True, hr_confirm = False) |
            Q(is_send_to_div=True,is_approve=True, hr_confirm=False)|
            Q(is_send_to_div=True,is_done=False, is_finish=False)|
            Q(is_approve=True, hr_confirm=False), is_cancel=False
        ).order_by('-pk')
    context = {
        'legend': 'Lista pedido Licensa','title': 'Lista pedido Licensa',
        'objects': leave

    }
    return render(request, 'notification/hr/leave.html', context)


@login_required
@allowed_users(allowed_roles=['hr','de','deputy'])
def PerformList(request):
    group = request.user.groups.all()[0].name
    paramas = ParameterA.objects.filter().all()
    parambs = ParameterB.objects.filter().all()
    years = EvalYear.objects.filter().all().order_by('year')
    employee = Employee.objects.filter(status_id=1).exclude(curempdivision__de__pk=1)
    ayear = EvalYear.objects.filter(is_active=True).last()
    objects = []
    for emp in employee:
        evalplan = EvalPlanning.objects.filter(employee=emp, year=ayear).last()
        evalpreass = EvalPreAssessment.objects.filter(employee=emp, year=ayear).last()
        check_plan = EvalPlanningA.objects.filter(eval=evalplan).exists()
        evalself = EvalSelf.objects.filter(employee=emp, year=ayear).last()
        eval = Eval.objects.filter(employee=emp, year=ayear).last()
        
        if eval:
            if eval.is_finish == False:
                objects.append([emp,evalplan, evalpreass, check_plan, evalself, eval])


    context = {
		'group': group, 'years': years, 'paramas': paramas, 'parambs': parambs,
		'title': 'Lista Avaliasaun', 'legend': 'Lista Avaliasaun', \
		'objects': objects, 'ayear':ayear.year
	}
    return render(request, 'notification/hr/evaluation.html', context)


@login_required
@allowed_users(allowed_roles=['admin','hr'])
def LeaveEndList(request):
    objects = []
    todayYear = datetime.today().date()
    employee = Employee.objects.filter(status_id=1)
    for obj in employee:
        period = LeavePeriod.objects.filter(employee=obj, is_active=True).last()
        if period:    
            if todayYear >= period.end_date:
                objects.append([obj, period])
                
    context = {
        'legend': 'Lista funsionario nebe licensa mate','title': 'Lista funsionario nebe licensa mate',
        'objects': objects, 'today': datetime.today().date()
    }
    return render(request, 'notification/hr/leave_end.html', context)


# done: Notif DEP
@login_required
@allowed_users(allowed_roles=['dep'])
def depNotifAllBadge(request):
    c_emp = c_staff(request.user)
    leave = 0
    leave = LeaveDep.objects.filter( 
        Q(leave__is_send=True, leave__dep_send=False,leave__dep_send_pr=False, leave__is_finish=False, leave__employee__curempdivision__department=c_emp.curempdivision.department)| \
        Q(leave__employee=c_emp, leave__is_finish=True, leave__is_reject=True, leave__is_done=False)| \
        Q(leave__employee=c_emp, leave__is_finish=True,  leave__is_done=False), leave__is_cancel=False 

        )\
        .all().count()
    dt_tot =  leave 
    return JsonResponse({'value':dt_tot})

@login_required
@allowed_users(allowed_roles=['dep'])
def depNotifEachBadge(request):
    c_emp = c_staff(request.user)
    leave = 0
    leave = LeaveDep.objects.filter( 
        Q(leave__is_send=True, leave__dep_send=False,leave__dep_send_pr=False, leave__is_finish=False, leave__employee__curempdivision__department=c_emp.curempdivision.department)| \
        Q(leave__employee=c_emp, leave__is_finish=True, leave__is_reject=True, leave__is_done=False)|\
        Q(leave__employee=c_emp, leave__is_finish=True,  leave__is_done=False), leave__is_cancel=False 
        )\
        .all().count()
    return JsonResponse({'data1':leave})




@login_required
@allowed_users(allowed_roles=['dep'])
def depLeaveList(request):
    c_emp = c_staff(request.user)
    leave = LeaveDep.objects.filter( 
        Q(leave__is_send=True, leave__dep_send=False,leave__dep_send_pr=False, leave__is_finish=False, leave__employee__curempdivision__department=c_emp.curempdivision.department)| \
        Q(leave__employee=c_emp, leave__is_finish=True, leave__is_reject=True, leave__is_done=False)| \
        Q(leave__employee=c_emp, leave__is_finish=True,  leave__is_done=False), leave__is_cancel=False 

        )\
        .all()
                
    context = {
        'legend': 'Lista Pedido husu Licensa','title': 'Lista Pedido husu Licensa',
        'objects': leave, 'today': datetime.today().date()
    }
    return render(request, 'notification/dep/leave.html', context)

# done: DIV
@login_required
@allowed_users(allowed_roles=['unit'])
def divNotifAllBadge(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q((Q(employee__curempdivision__department__unit=unit)|Q(employee__curempdivision__unit=unit))
        ,dep_send=True,unit_send=False, is_finish=False)| \
        Q(pr_send=True, is_done=False, employee=emp_unit)|  
        Q(Q(employee__curempdivision__unit=unit), is_send_to_div=True, is_finish=False),is_cancel=False
        ).all().count()
    dt_tot =  leave 
    return JsonResponse({'value':dt_tot})

@login_required
@allowed_users(allowed_roles=['unit'])
def divNotifEachBadge(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q((Q(employee__curempdivision__department__unit=unit)|Q(employee__curempdivision__unit=unit))
        ,dep_send=True,unit_send=False, is_finish=False)| \
        Q(pr_send=True, is_done=False,employee=emp_unit)|
        Q(Q(employee__curempdivision__unit=unit), is_send_to_div=True, is_finish=False), is_cancel=False
        ).all().count()
    return JsonResponse({'data1':leave})


@login_required
@allowed_users(allowed_roles=['unit'])
def divLeaveList(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = Leave.objects.filter(
        Q((Q(employee__curempdivision__department__unit=unit)|Q(employee__curempdivision__unit=unit))
        ,dep_send=True,unit_send=False, is_finish=False)| \
        Q(pr_send=True, is_done=False, employee=c_emp)|
        Q(Q(employee__curempdivision__unit=unit), is_send_to_div=True, is_finish=False), is_cancel=False
        ).all()
                
    context = {
        'legend': 'Lista Pedido husu Licensa','title': 'Lista Pedido husu Licensa',
        'objects': leave, 'today': datetime.today().date()
    }
    return render(request, 'notification/div/leave.html', context)



# done: PRESIDENTE
@login_required
@allowed_users(allowed_roles=['de'])
def prNotifAllBadge(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q(dep_send=True,unit_send=False, is_finish=False)| \
        Q(unit_send_pr=True, pr_send=False)| \
        Q(dep_send_pr=True, pr_send=False), is_cancel=False
        ).all().count()
    dt_tot =  leave 
    return JsonResponse({'value':dt_tot})

@login_required
@allowed_users(allowed_roles=['de'])
def prNotifEachBadge(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q(dep_send=True,unit_send=False, is_finish=False)| \
        Q(unit_send_pr=True, pr_send=False)|\
        Q(dep_send_pr=True, pr_send=False), is_cancel=False
        ).all().count()
    return JsonResponse({'data1':leave})


@login_required
@allowed_users(allowed_roles=['de'])
def prLeaveList(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = Leave.objects.filter(
        Q(dep_send=True,unit_send=False, is_finish=False)| \
        Q(unit_send_pr=True, pr_send=False)|\
        Q(dep_send_pr=True, pr_send=False), is_cancel=False
        ).order_by('-pk')
                
    context = {
        'legend': 'Lista Pedido husu Licensa','title': 'Lista Pedido husu Licensa',
        'objects': leave, 'today': datetime.today().date()
    }
    return render(request, 'notification/pr/leave.html', context)



# done: VICE
@login_required
@allowed_users(allowed_roles=['deputy'])
def viceNotifAllBadge(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q(pr_send=True, is_done=False, employee=emp_unit)|\
        Q(pr_notify=True,hr_confirm = False), is_cancel=False
        ).all().count()
    dt_tot =  leave 
    return JsonResponse({'value':dt_tot})

@login_required
@allowed_users(allowed_roles=['deputy'])
def viceNotifEachBadge(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q(pr_send=True, is_done=False,employee=emp_unit)|\
        Q(pr_notify=True,hr_confirm = False), is_cancel=False).all().count()
    return JsonResponse({'data1':leave})


@login_required
@allowed_users(allowed_roles=['deputy'])
def viceLeaveList(request):
    c_emp = c_staff(request.user)
    emp_unit, unit = c_unit(request.user)
    leave = Leave.objects.filter(
        Q(pr_send=True, is_done=False, employee=c_emp)|\
        Q(pr_notify=True,hr_confirm = False), is_cancel=False).all()
                
    context = {
        'legend': 'Lista Pedido husu Licensa','title': 'Lista Pedido husu Licensa',
        'objects': leave, 'today': datetime.today().date()
    }
    return render(request, 'notification/vice/leave.html', context)




# done: STAFF
@login_required
@allowed_users(allowed_roles=['staff'])
def staffNotifAllBadge(request):
    c_emp = c_staff(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q(employee=c_emp, is_finish=True, is_done=False, is_reject=True)| \
        Q(employee=c_emp, is_finish=True, pr_send=True, is_done=False)| \
        Q(employee=c_emp, is_finish=True, unit_send=True, is_done=False)
    ).all().count()
    dt_tot =  leave 
    return JsonResponse({'value':dt_tot})

@login_required
@allowed_users(allowed_roles=['staff'])
def staffNotifEachBadge(request):
    c_emp = c_staff(request.user)
    leave = 0
    leave = Leave.objects.filter(
        Q(employee=c_emp, is_finish=True, is_done=False, is_reject=True)| \
        Q(employee=c_emp, is_finish=True, pr_send=True, is_done=False)|\
        Q(employee=c_emp, is_finish=True, unit_send=True, is_done=False)
    ).all().count()
    return JsonResponse({'data1':leave})

@login_required
@allowed_users(allowed_roles=['staff'])
def staffLeaveList(request):
    c_emp = c_staff(request.user)
    leave = Leave.objects.filter(
        Q(employee=c_emp, is_finish=True, is_done=False, is_reject=True)| \
        Q(employee=c_emp, is_finish=True, pr_send=True, is_done=False)|\
        Q(employee=c_emp, is_finish=True, unit_send=True, is_done=False)

    ).all()
                
    context = {
        'legend': 'Lista Notifikasaun Licensa','title': 'Lista Notifikasaun Licensa',
        'objects': leave, 'today': datetime.today().date()
    }
    return render(request, 'notification/staff/leave.html', context)


