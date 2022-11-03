from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.db.models import F, Q, Sum
from django.http import Http404
from .models import *
from .forms import *
from .decorators import allowed_users
from datetime import datetime, date


#  SEVERAL
def client_detail(request, id):
    ctx = {}
    client = Clients.objects.get(id=id)
    ctx['clients'] = client

    return HttpResponse(f'Client: {client}')


@allowed_users(allowed_roles=['client', 'manager'])
# @permission_required('agency_site.view_type_of_order', raise_exception=True)
def pricelist(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    types = TypeOfOrder.objects.all()
    ctx['types'] = types

    return render(request, 'pricelist.html', ctx)


@allowed_users(allowed_roles=['manager', 'chief', 'detective', 'assistant'])
def clients_info(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    clients = Clients.objects.all()
    ctx['clients'] = clients

    return render(request, 'several/all_clients.html', ctx)


@allowed_users(allowed_roles=['chief', 'detective'])
def all_employees(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    employees = Employees.objects.all()
    ctx['employees'] = employees

    return render(request, 'several/all_employees.html', ctx)


def registration_page(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        client_form = ClientProfileForm(request.POST)

        if form.is_valid() and client_form.is_valid():
            print('user form:', form.errors, 'client form', client_form.errors)
            user = form.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            group = Group.objects.get(name='client')
            group.user_set.add(user)
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('test-client-login')
        else:
            print('NOT VALID')
    else:
        form = ExtendedUserCreationForm()
        client_form = ClientProfileForm()

    ctx = {'form': form, 'client_form': client_form}
    return render(request, 'client/test-registration.html', ctx)


# @unauthenticated_user
def test_login(request):
    ctx = {}
    if request.method == 'POST':
        form = TestClientLogin(request.POST)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('OK')
            login(request, user)
            # print(str(request.user.groups.get()))
            try:
                if str(request.user.groups.get()) == 'manager':
                    return redirect('manager-page')
                elif str(request.user.groups.get()) == 'client':
                    return redirect('test-client-page')
                elif str(request.user.groups.get()) == 'chief':
                    return redirect('chief-page')
                elif str(request.user.groups.get()) == 'detective':
                    return redirect('detective-page')
                elif str(request.user.groups.get()) == 'assistant':
                    return redirect('assistant-page')
                elif str(request.user.groups.get()) == 'admin':
                    return redirect('admin:index')
            except:

                raise Http404('Something has gone wrong!Please, try later.')
        else:
            print('NO such user')
            return redirect('test-client-login')

    else:
        form = TestClientLogin()
    ctx['form'] = form
    return render(request, 'client/client-login.html', ctx)


def test_client_logout(request):
    logout(request)
    return redirect('test-client-login')


# CLIENT


@allowed_users(allowed_roles=['client'])
@permission_required('agency_site.add_orders', raise_exception=True)
def test_create_order(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':
        form = TestCreateOrder(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            client_comment = cleaned_data['client_comment']
            o_type = cleaned_data['type_of_order']
            client_pk = Clients.objects.get(pk=request.user.clients.pk)

            new_order = Orders(

                client_comment=client_comment,
                type_of_order=o_type,
                client=client_pk

            )
            new_order.save()
            return redirect('test-client-page')
        else:
            ctx['form'] = form
    else:
        form = TestCreateOrder()
    ctx['form'] = form

    return render(request, 'client/create-order.html', ctx)


# @login_required(login_url='client-login')
@allowed_users(allowed_roles=['client'])
def test_client_page(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    #
    new_orders = request.user.clients.orders_set.filter(status='In process')
    orders_on_review = request.user.clients.orders_set.exclude(status='Closed').exclude(status='In process')

    prices_qs = request.user.clients.orders_set.exclude(status='Closed').exclude(status='In process').aggregate(
        total_price=Sum(F('type_of_order__price') * F('rate')))

    # Check this two cycles later - probably dont need them more
    ar = []
    for ord in request.user.clients.orders_set.all():
        ar.append(ord.rate)
    for tor in request.user.clients.orders_set.aggregate(total_price=Sum(F('type_of_order__price') * F('rate'))):
        ar.append(tor)

    ctx['new_orders'] = new_orders
    ctx['orders_on_review'] = orders_on_review
    ctx['total'] = prices_qs['total_price']

    return render(request, 'client/client_page.html', ctx)


@allowed_users(allowed_roles=['client'])
@permission_required('agency_site.change_orders', raise_exception=True)
def client_pays_for_order(request, id):

    new_status = Orders.objects.get(id=id)
    new_status.status = 'Payed'
    new_status.save()
    return redirect('test-client-page')


@allowed_users(allowed_roles=['client'])
@permission_required('agency_site.add_orders', raise_exception=True)
def client_rejects_order(request, id):

    new_status = Orders.objects.get(id=id)
    new_status.status = 'Rejected by client'
    new_status.save()
    return redirect('test-client-page')


@allowed_users(allowed_roles=['client'])
def history_of_orders(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    orders = Orders.objects.filter(client=request.user.clients.pk).order_by('-created_at')
    reports = Report.objects.all()

    print('rep : ', reports)
    ctx['orders'] = orders
    ctx['reports'] = reports
    return render(request, 'client/history_of_orders.html', ctx)


@allowed_users(allowed_roles=['client'])
def client_view_report(request, pk):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    this_report = Report.objects.get(pk=pk)
    ctx['this_report'] = this_report
    return render(request,  'client/client-view-report.html', ctx)


# MANAGER


@allowed_users(allowed_roles=['manager'])
def manager_page(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    orders_in_process = Orders.objects.filter(status='In process')
    personal_orders = Orders.objects.filter(manager=request.user.employees.pk)

    ctx['personal_orders'] = personal_orders
    ctx['orders_in_process'] = orders_in_process
    ctx['new_orders'] = Orders.objects.filter(created_at=date.today()).count()
    print('DATE', date.today())

    return render(request, 'manager/manager-page.html', ctx)


@allowed_users(allowed_roles=['manager'])
@permission_required('agency_site.change_orders', raise_exception=True)
def take_order(request, id):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':

        new_rate = request.POST.get('rate')
        manager = Employees.objects.get(pk=request.user.employees.pk)
        order_detail = Orders.objects.get(id=id)
        ctx['order_detail'] = order_detail

        modified_order = order_detail
        modified_order.rate = int(new_rate)
        modified_order.manager = manager
        modified_order.status = 'Pending client'
        modified_order.save()  # Обновляем заявку(обновляем rate, меняем статус заказа и привязываем менеджера к заявке)

        if manager.status == 'Available':
            manager.status = 'Busy'
            manager.save()

        print('saved')
        return redirect('manager-page')

    else:
        print('get')
        order_detail = Orders.objects.get(id=id)
        ctx['order_detail'] = order_detail

    return render(request, 'manager/take-order.html', ctx)


@allowed_users(allowed_roles=['manager'])
@permission_required('agency_site.change_orders', raise_exception=True)
def reject_order_manager(request, id):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    manager = Employees.objects.get(pk=request.user.employees.pk)
    current_order = Orders.objects.get(id=id)

    current_order.manager = manager
    current_order.status = 'Rejected by manager'
    current_order.save()

    return redirect('manager-page')


# CHIEF


@allowed_users(allowed_roles=['chief'])
def chief_main_page(request):
    ctx = {}
    group =  str(request.user.groups.get())
    ctx['group'] = group

    today_orders = Orders.objects.filter(created_at=date.today()).count()
    ctx['today_orders'] = today_orders

    finished_orders = Orders.objects.filter(created_at=date.today(), status='Closed').count()
    ctx['finished_orders'] = finished_orders

    current_month = datetime.now().month
    current_year = datetime.now().year

    # For managers table

    # stores pk of managers
    managers_pk = []
    # stores pk of employee(manager) as key and employees fields as value
    managers_info = {}

    [managers_pk.append(manager.pk) for manager in Employees.objects.filter(position='Manager')]

    for pk in managers_pk:
        managers_info[pk] = Employees.objects.filter(pk=pk)

    count_orders_for_each_manager = {}
    for pk in managers_info:
        count_orders_for_each_manager[pk] = \
            Orders.objects.filter(manager=pk, created_at__month=current_month, created_at__year=current_year).count()

    count_closed_orders_for_each_manager = {}
    for pk in managers_info:
        count_closed_orders_for_each_manager[pk] = \
            Orders.objects.filter(manager=pk, created_at__month=current_month,
                                  created_at__year=current_year, status='Closed').count()

    # For detectives table

    # stores pk of detectives
    detectives_pk = []
    # stores pk of employee(detective) as key and employees fields as value
    detectives_info = {}

    [detectives_pk.append(detective.pk) for detective in Employees.objects.filter(position='Detective')]

    for pk in detectives_pk:
        detectives_info[pk] = Employees.objects.filter(pk=pk)

    count_orders_for_each_detective = {}
    for pk in detectives_info:
        count_orders_for_each_detective[pk] = \
            Orders.objects.filter(detective=pk, created_at__month=current_month, created_at__year=current_year).count()

    count_closed_orders_for_each_detective = {}
    for pk in detectives_info:
        count_closed_orders_for_each_detective[pk] = \
            Orders.objects.filter(detective=pk, created_at__month=current_month,
                                  created_at__year=current_year, status='Closed').count()

    ctx['managers_info'] = managers_info
    ctx['count_orders_for_each_manager'] = count_orders_for_each_manager
    ctx['count_closed_orders_for_each_manager'] = count_closed_orders_for_each_manager

    ctx['detectives_info'] = detectives_info
    ctx['count_orders_for_each_detective'] = count_orders_for_each_detective
    ctx['count_closed_orders_for_each_detective'] = count_closed_orders_for_each_detective

    return render(request, 'chief/chief-page.html', ctx)


@allowed_users(allowed_roles=['chief'])
def accumulative_sum(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    qs = Orders.objects.values('created_at__month').filter(
        Q(status='Closed') | Q(status='Payed') | Q(status='In work')).annotate(
        tot=(Sum(F('rate') * F('type_of_order_id__price')))).order_by('created_at__month')

    qs = qs.values_list('created_at__month', 'tot')
    profit_for_month_and_acc_sum = {}

    totSum = 0
    for month, profit in qs:
        totSum += profit
        profit_for_month_and_acc_sum[month] = [profit, totSum]

    ctx['acc_sum'] = profit_for_month_and_acc_sum

    return render(request, 'chief/accumulative_sum.html', ctx)


@allowed_users(allowed_roles=['chief'])
def count_income_for_specific_type_of_order(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    if request.method == 'POST':
        types_of_orders = TypeOfOrder.objects.values('type')
        types = []
        for key in types_of_orders:
            for value in key:
                types.append(key[value])
        ctx['types'] = types

        selected_type = request.POST.get('type')
        selected_type_pk = TypeOfOrder.objects.get(type=selected_type)
        qs = Orders.objects.filter(Q(status='Closed') | Q(status='Payed') | Q(status='In work'),
                                   type_of_order__id=selected_type_pk.pk).aggregate(
            tot_income=(Sum(F('type_of_order_id__price') * F('rate'))))

        if qs['tot_income'] is None:
            qs['tot_income'] = 0

        ctx['income_for_type'] = qs['tot_income']
        ctx['selected_type'] = selected_type

        return render(request, 'chief/count_income_for_specific_type.html', ctx)

    else:

        types_of_orders = TypeOfOrder.objects.values('type')
        types = []
        for key in types_of_orders:
            for value in key:
                types.append(key[value])

        ctx['types'] = types

        return render(request, 'chief/count_income_for_specific_type.html', ctx)


@allowed_users(allowed_roles=['chief'])
def count_income(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':
        form = CalculateIncomeForPeriod(request.POST)
        print(form['start_date'])
        if form.is_valid():

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if end_date > datetime.now().date() or start_date > end_date:
                return redirect('chief-page')

            qs = Orders.objects.filter(created_at__range=(start_date, end_date)).aggregate(
             total_price=Sum(F('type_of_order__price') * F('rate')))

            ctx['total'] = qs['total_price']

            return render(request, 'chief/count-income.html', ctx)
        else:
            ctx['form'] = form
    else:
        form = CalculateIncomeForPeriod()
    ctx['form'] = form

    return render(request, 'chief/count-income.html', ctx)


@allowed_users(allowed_roles=['chief'])
def count_rejected_orders_by_clients(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':
        form = CalculateIncomeForPeriod(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if end_date > datetime.now().date() or start_date > end_date:
                return redirect('chief-page')
            rejected_by_client = Orders.objects.filter(created_at__range=(start_date, end_date),
                                                       status='Rejected by client').count()
            ctx['rejected_by_client'] = rejected_by_client

            return render(request, 'chief/count-rejected-orders-by-clients.html', ctx)
        else:
            ctx['form'] = form
    else:
        form = CalculateIncomeForPeriod()
    ctx['form'] = form

    return render(request, 'chief/count-rejected-orders-by-clients.html', ctx)


@allowed_users(allowed_roles=['chief'])
def count_new_orders_for_period(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':
        form = CalculateIncomeForPeriod(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if end_date > datetime.now().date() or start_date > end_date:
                return redirect('chief-page')
            new_orders_for_period = Orders.objects.filter(created_at__range=(start_date, end_date)).count()
            ctx['rejected_by_client'] = new_orders_for_period

            return render(request, 'chief/count-rejected-orders-by-clients.html', ctx)
        else:
            ctx['form'] = form
    else:
        form = CalculateIncomeForPeriod()
    ctx['form'] = form

    return render(request, 'chief/count-rejected-orders-by-clients.html', ctx)


@allowed_users(allowed_roles=['chief'])
def count_closed_orders_for_period_for_detectives(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':
        form = CalculateIncomeForPeriod(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # stores pk of detectives as key
            detectives_pk = []
            # stores pk of employee(detective) as key and employees fields as value
            detectives_info = {}
            [detectives_pk.append(detective.pk) for detective in Employees.objects.filter(position='Detective')]

            for pk in detectives_pk:
                detectives_info[pk] = Employees.objects.filter(pk=pk)

            count_orders_for_each_detective = {}
            for pk in detectives_info:
                count_orders_for_each_detective[pk] = \
                    Orders.objects.filter(detective=pk,
                                          created_at__range=(start_date, end_date), status='Closed').count()

            ctx['detectives_info'] = detectives_info
            ctx['count_orders_for_each_detective'] = count_orders_for_each_detective

            return render(request, 'chief/count_closed_orders_for_period_for_detectives.html', ctx)
        else:
            ctx['form'] = form
    else:
        form = CalculateIncomeForPeriod()
    ctx['form'] = form

    return render(request, 'chief/count_closed_orders_for_period_for_detectives.html', ctx)


@allowed_users(allowed_roles=['chief'])
@permission_required('agency_site.view_report', raise_exception=True)
def all_reports(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    reports = Report.objects.all()
    ctx['reports'] = reports

    return render(request, 'chief/all_reports.html', ctx)


# DETECTIVE

@allowed_users(allowed_roles=['detective'])
def detective_main_page(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    paid_orders = Orders.objects.filter(status='Payed', detective=None)
    ctx['paid_orders'] = paid_orders

    personal_orders = Orders.objects.filter(detective=request.user.employees.pk, status='In work')
    ctx['personal_orders'] = personal_orders

    return render(request, 'detective/detective-page.html', ctx)


@allowed_users(allowed_roles=['detective'])
@permission_required('agency_site.change_orders', raise_exception=True)
def detective_takes_order(request, pk):
    detective_pk = Employees.objects.get(pk=request.user.employees.pk)
    get_order = Orders.objects.get(pk=pk)

    new_detective = get_order
    new_detective.detective = detective_pk
    new_detective.save()

    get_order.status = 'In work'
    get_order.save()

    if detective_pk.status == 'Available':
        detective_pk.status = 'Busy'
        detective_pk.save()

    return redirect('detective-page')


@allowed_users(allowed_roles=['detective'])
@permission_required('agency_site.add_report', raise_exception=True)
def detective_makes_report(request, pk):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    order_detail = Orders.objects.get(pk=pk)
    ctx['order_detail'] = order_detail
    if request.method == 'POST':
        order_detail = Orders.objects.get(pk=pk)
        new_report = Report(
            orders=order_detail,
            detective_report=request.POST.get('detectives_report')
        )
        new_report.save()

        order_detail.status = 'Closed'
        order_detail.save()

        detective = Employees.objects.get(pk=request.user.employees.pk)
        if Orders.objects.filter(detective=detective.pk, status='Payed').count() == 0:
            detective.status = 'Available'
            detective.save()

        return redirect('detective-page')

    return render(request, 'detective/detective_makes_report.html', ctx)


@allowed_users(allowed_roles=['detective'])
def detective_show_client_comment(request, pk):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    this_order = Orders.objects.get(pk=pk)
    ctx['this_order'] = this_order

    return render(request, 'detective/detective_show_client_comment.html', ctx)


# ОЧЕНЬ КОРЯВО
@allowed_users(allowed_roles=['detective'])
@permission_required('agency_site.add_tasks', raise_exception=True)
def detective_assign_task(request, pk):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    assistants = Employees.objects.filter(chief_id=request.user.employees.pk)
    ctx['assistants'] = assistants

    types = []
    for key in assistants:
        # for value in key:
        types.append(key)

    ctx['types'] = types
    print(types)
    if request.method == 'POST':
        selected_assistant = request.POST.get('type')
        set_assistant = Employees.objects.get(pk=selected_assistant)
        task = request.POST.get('assign_task')
        new_task = Tasks(
                    task_description=task,
                    employees=set_assistant,
                    orders=Orders.objects.get(pk=pk)
                )
        new_task.save()

        return redirect('detective-page')

    return render(request, 'detective/detective_assign_task.html', ctx)


@allowed_users(allowed_roles=['detective'])
def detective_history_of_orders(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    detective_orders = Orders.objects.filter(detective=request.user.employees.pk).order_by('-created_at')
    ctx['detective_orders'] = detective_orders

    return render(request, 'detective/detective_history_of_orders.html', ctx)


@allowed_users(allowed_roles=['detective'])
def detective_assistants(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    detective_assistants_all = Employees.objects.filter(chief=request.user.employees.pk)
    ctx['detective_assistants_all'] = detective_assistants_all

    assistant_tasks = Tasks.objects.filter(employees=Employees.objects.filter(position='Assistant'))

    ctx['assistant_tasks'] = assistant_tasks

    return render(request, 'detective/detective-assistants.html', ctx)


@allowed_users(allowed_roles=['detective'])
@permission_required('agency_site.view_tasks', raise_exception=True)
def detective_assistant_tasks(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    tasks = Tasks.objects.all()
    ctx['tasks'] = tasks
    comments = Assistant_comments.objects.all()

    ctx['comments'] = comments

    return render(request, 'detective/detective-assistant-tasks.html', ctx)


@allowed_users(allowed_roles=['detective'])
def detective_show_assistant_comment(request, pk):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    assistant_comment = Assistant_comments.objects.filter(task=pk)
    ctx['assistant_comment'] = assistant_comment

    return render(request, 'detective/show_assistant_comment.html', ctx)


@allowed_users(allowed_roles=['detective'])
@permission_required('agency_site.delete_tasks', raise_exception=True)
def detective_delete_task(request, pk):
    task = Tasks.objects.get(pk=pk)
    task.delete()

    return redirect('detective-assistant-tasks')


# ASSISTANT


@allowed_users(allowed_roles=['assistant'])
def assistant_page(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    assistant_tasks = Tasks.objects.filter(employees=request.user.employees.pk, )
    ctx['assistant_tasks'] = assistant_tasks

    return render(request, 'assistant/assistant-page.html', ctx)


@allowed_users(allowed_roles=['assistant'])
def left_comment_for_task(request, pk):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group
    if request.method == 'POST':
        new_comment = request.POST.get('new_comment')
        if new_comment is None:
            return redirect(f'assistant-left-comment/{pk}')

        new_assistant_comment = Assistant_comments(

            assistant_comments=new_comment,
            task=Tasks.objects.get(pk=pk),
            employees=Employees.objects.get(pk=request.user.employees.pk)
        )
        new_assistant_comment.save()

        assistant = Employees.objects.get(pk=request.user.employees.pk)

        if Tasks.objects.filter(employees=assistant).count() == 0:
            assistant.status = 'Available'
            assistant.save()

        return redirect('assistant-page')

    return render(request,  'assistant/assistant_left_comment.html', ctx)


@allowed_users(allowed_roles=['assistant'])
def history_of_finished_tasks(request):
    ctx = {}
    group = str(request.user.groups.get())
    ctx['group'] = group

    finished_tasks = Assistant_comments.objects.filter(employees=request.user.employees.pk)
    print(request.user.employees.pk)

    ctx['finished_tasks'] = finished_tasks

    return render(request, 'assistant/assistant_history_of_finished_tasks.html', ctx)


