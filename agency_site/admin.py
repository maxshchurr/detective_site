from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as DjangoUser

from .models import Employees, Clients, Orders, TypeOfOrder, Report, Tasks, Assistant_comments


class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('surname', 'first_name')


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'tel_number', 'email')


# class OrdersAdmin(admin.ModelAdmin):
#     list_display = ('client_comment', 'created_at')
#
#
# class TypeOfOrderAdmin(admin.ModelAdmin):
#     list_display = ('type', 'price', 'expected_days')
#
#
# class ReportAdmin(admin.ModelAdmin):
#     list_display = ('detective_report', 'report_date', 'orders')
#
#
# class TasksAdmin(admin.ModelAdmin):
#     list_display = ['employees', 'orders', 'task_date']
#
#
# class AssistantCommentsAdmin(admin.ModelAdmin):
#     list_display = ['employees', 'task', 'assistant_comments']


admin.site.register(Employees, EmployeesAdmin)

admin.site.register(Clients, ClientsAdmin)

# admin.site.register(Orders, OrdersAdmin)
#
# admin.site.register(TypeOfOrder, TypeOfOrderAdmin)
#
# admin.site.register(Report, ReportAdmin)
#
# admin.site.register(Tasks, TasksAdmin)
#
# admin.site.register(Assistant_comments, AssistantCommentsAdmin)


