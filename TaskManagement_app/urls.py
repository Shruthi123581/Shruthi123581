from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .import AdminViews, TeamheadViews, TeammemViews
from .TeamheadViews import ProjectList, ProjectDetail, ProjectCreate, ProjectUpdate, DeleteView, TaskList, TaskDetail, TaskCreate, TaskUpdate

urlpatterns = [
     
    
    path('', views.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    path('add_head/', AdminViews.add_head, name="add_head"),
    path('add_head_save/', AdminViews.add_head_save, name="add_head_save"),
    path('manage_head/', AdminViews.manage_head, name="manage_head"),
    path('edit_head/<head_id>/', AdminViews.edit_head, name="edit_head"),
    path('edit_head_save/', AdminViews.edit_head_save, name="edit_head_save"),
    path('delete_head/<head_id>/', AdminViews.delete_head, name="delete_head"),

    path('add_member/', AdminViews.add_member, name="add_member"),
    path('add_mem_save/', AdminViews.add_mem_save, name="add_mem_save"),
    path('edit_member/<member_id>', AdminViews.edit_member, name="edit_member"),
    path('edit_member_save/', AdminViews.edit_member_save, name="edit_member_save"),
    path('manage_member/', AdminViews.manage_member, name="manage_member"),
    path('delete_member/<member_id>/', AdminViews.delete_member, name="delete_member"),
    path('check_email_exist/', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', AdminViews.check_username_exist, name="check_username_exist"),
    path('admin_profile/', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', AdminViews.admin_profile_update, name="admin_profile_update"),
    
    path('feedback_message/', AdminViews.feedback_message, name="feedback_message"),
    path('feedback_message_reply/', AdminViews.feedback_message_reply, name="feedback_message_reply"),
    path('leave_view/', AdminViews.leave_view, name="leave_view"),
    path('leave_approve/<leave_id>/', AdminViews.leave_approve, name="leave_approve"),
    path('leave_reject/<leave_id>/', AdminViews.leave_reject, name="leave_reject"),

    path('head_home/', TeamheadViews.head_home, name="head_home"),
    path('head_profile/', TeamheadViews.head_profile, name="head_profile"),
    path('head_profile_update/', TeamheadViews.head_profile_update, name="head_profile_update"),
    path('apply_leave/', TeamheadViews.apply_leave, name="apply_leave"),
    path('apply_leave_save/', TeamheadViews.apply_leave_save, name="apply_leave_save"),
    path('feedback/', TeamheadViews.feedback, name="feedback"),
    path('feedback_save/', TeamheadViews.feedback_save, name="feedback_save"),



    path('member_home/', TeammemViews.member_home, name="member_home"),
    path('member_profile/', TeammemViews.member_profile, name="member_profile"),
    path('member_profile_update/', TeammemViews.member_profile_update, name="member_profile_update"),
    path('member_view_task/', TeammemViews.member_view_task, name="member_view_task"),
    path('profile/', TeammemViews.profile, name="profile"),
    path('apply_leave1/', TeammemViews.apply_leave1, name="apply_leave1"),
    path('apply_leave_save1/', TeammemViews.apply_leave_save1, name="apply_leave_save1"),
    path('feedback1/', TeammemViews.feedback1, name="feedback1"),
    path('feedback_save1/', TeammemViews.feedback_save1, name="feedback_save1"),
    path('task/<int:task_id>/update-status/',TeammemViews.update_task_status, name='update_task_status'),
    #path('update-task-status/<int:task_id>/', TeammemViews.update_task_status, name='update_task_status'),
    path('member_task_list/', TeammemViews.member_task_list, name='member_task_list'),
    path('member_projects/', TeammemViews.member_projects, name='member_projects'),
    path('get_tasks/', TeammemViews.get_tasks, name='get_tasks'),
   

     path('projects', ProjectList.as_view(), name='projects'),
	path('project/<int:pk>/', ProjectDetail.as_view(), name='project'),
	path('create-project/', ProjectCreate.as_view(), name='project-create'),
	path('project-update/<int:pk>/', ProjectUpdate.as_view(), name='project-update'),
	path('project-delete/<int:pk>/', DeleteView.as_view(), name='project-delete'),

	path('task-list/', TaskList.as_view(), name='tasks'),
	path('create-task/', TaskCreate.as_view(), name='task-create'),
	path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
 
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
         name="reset_password"),
    
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
         name="password_reset_done"),
    
    path('reset/<uidb64>/<token>', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
         name="password_reset_confirm"),
    
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
         name="password_reset_complete"),



   ]