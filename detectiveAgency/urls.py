"""detectiveAgency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from agency_site import views

admin.site.site_header = "Detective agency admin"
admin.site.site_title = "Detective agency admin"
admin.site.index_title = "Welcome to Magnum detective agency administration panel"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('registration-page/', views.registration_page, name='registration-page'),

    # CLIENTS
    path('test-client-login/', views.test_login, name='test-client-login'),
    path('test-client-page/', views.test_client_page, name='test-client-page'),
    path('client-pays-for-order/<int:id>', views.client_pays_for_order, name='client-pays-for-order'),
    path('client-rejects-order/<int:id>', views.client_rejects_order, name='client-rejects-order'),
    path('client/orders-history', views.history_of_orders, name='orders-history'),
    path('client/view-report/<int:pk>', views.client_view_report, name='client-view-report'),


    # MANAGER
    path('manager-page', views.manager_page, name='manager-page'),
    path('manager-page/<int:id>', views.take_order, name='take-order-manager'),
    path('reject-order-manager/<int:id>', views.reject_order_manager, name='reject-order-manager'),


    # CHIEF
    path('chief-page', views.chief_main_page, name='chief-page'),
    path('count-income', views.count_income, name='count-income'),
    path('count-rejected-orders/', views.count_rejected_orders_by_clients, name='count-rejected-orders'),
    path('chief/count-new-orders-for-period/', views.count_new_orders_for_period, name='count-new-orders-for-period'),
    path('chief/all-reports/', views.all_reports, name='all-reports'),
    path('chief/count_closed_orders_for_period_for_detectives', views.count_closed_orders_for_period_for_detectives,
         name='closed-orders-for-period-for-detectives'),

    path('chief/accumulative-sum', views.accumulative_sum, name='accumulative-sum'),
    path('chief/count-income-for-specific-type', views.count_income_for_specific_type_of_order,
         name='count-income-for-specific-type'),


    # DETECTIVE
    path('detective-page/', views.detective_main_page, name='detective-page'),
    path('detective-takes-order/<int:pk>/', views.detective_takes_order, name='detective-takes-order'),
    path('detective-makes-report/<int:pk>/', views.detective_makes_report, name='detective-makes-report'),
    path('detective-assign-task/<int:pk>', views.detective_assign_task, name='detective-assign-task'),
    path('detective-show-client-comment/<int:pk>', views.detective_show_client_comment,
         name='detective-show-client-comment'),
    path('detective-history-of-orders/', views.detective_history_of_orders, name='detective-history-of-orders'),
    path('detective-assistants/', views.detective_assistants, name='detective-assistants'),
    path('detective-assistant-tasks/', views.detective_assistant_tasks, name='detective-assistant-tasks'),
    path('detective-show-assistant-comment/<int:pk>', views.detective_show_assistant_comment,
         name='show-assistant-comment'),
    path('detective-delete-task/<int:pk>', views.detective_delete_task, name='detective-delete-task'),


    # ASSISTANT
    path('assistant-page/', views.assistant_page, name='assistant-page'),
    path('assistant/assistant-left-comment/<int:pk>/', views.left_comment_for_task, name='assistant-left-comment'),
    path('assistant/assistant-history-of-finished-tasks/', views.history_of_finished_tasks,
         name='assistant-history-of-finished-tasks'),


    # SEVERAL
    path('all-clients/', views.clients_info, name='all-clients'),
    path('client-detail/<int:id>/', views.client_detail, name='client-detail'),
    path('pricelist', views.pricelist, name='pricelist'),
    path('all-employees/', views.all_employees, name='all-employees'),


    # TO BE DONE
    path('test-client-order/', views.test_create_order, name='create-order-client'),
    path('client-logout/', views.test_client_logout, name='client-logout'),



]

