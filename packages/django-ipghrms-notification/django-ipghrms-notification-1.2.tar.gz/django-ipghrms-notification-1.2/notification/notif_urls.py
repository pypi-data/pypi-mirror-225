from django.urls import path
from notification import views

urlpatterns = [
    # done: HR
    path('hr/all/', views.hrNotifAllBadge, name='hr-notif-all'),
    path('hr/badge/', views.hrNotifEachBadge, name='hr-notif-badge-all'),


    path('hr/end/contract/list/', views.EndContractList, name='end-contract-list'),
    path('hr/birthday/list/', views.BirthdayList, name='birthday-list'),
    path('hr/leave/list/', views.LeaveList, name='leave-list'),
    path('hr/evaluation/list/', views.PerformList, name='evaluation-list'),
    path('hr/leave/end/list/', views.LeaveEndList, name='leave-end-list'),


    # done: DEP
    path('dep/all/', views.depNotifAllBadge, name='dep-notif-all'),
    path('dep/badge/', views.depNotifEachBadge, name='dep-notif-badge-all'),
    path('dep/leave/list/', views.depLeaveList, name='dep-leave-list'),
    
    
    # done: DIV
    path('div/all/', views.divNotifAllBadge, name='div-notif-all'),
    path('div/badge/', views.divNotifEachBadge, name='div-notif-badge-all'),
    path('div/leave/list/', views.divLeaveList, name='div-leave-list'),


    # done: STAFF
    path('staff/all/', views.staffNotifAllBadge, name='staff-notif-all'),
    path('staff/badge/', views.staffNotifEachBadge, name='staff-notif-badge-all'),
    path('staff/leave/list/', views.staffLeaveList, name='staff-leave-list'),
    
    # done: PR
    path('pr/all/', views.prNotifAllBadge, name='pr-notif-all'),
    path('pr/badge/', views.prNotifEachBadge, name='pr-notif-badge-all'),
    path('pr/leave/list/', views.prLeaveList, name='pr-leave-list'),
    
    
    # done: VICE
    path('vice/all/', views.viceNotifAllBadge, name='vice-notif-all'),
    path('vice/badge/', views.viceNotifEachBadge, name='vice-notif-badge-all'),
    path('vice/leave/list/', views.viceLeaveList, name='vice-leave-list'),

]

