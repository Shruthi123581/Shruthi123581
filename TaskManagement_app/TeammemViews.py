from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from TaskManagement_app.models import CustomUser, TeamHead, TeamMem,Project,Task,FeedBack,LeaveReport
from django.shortcuts import render, get_object_or_404
from docx import Document
from .forms import TaskStatusUpdateForm
import os
from django.http import JsonResponse

def member_home(request):
    team_member = TeamMem.objects.get(admin=request.user)
    tasks = Task.objects.filter(assigned_member=team_member)
    
    # Separate tasks based on their status
    all_tasks = tasks
    completed_tasks = tasks.filter(task_status='3')
    in_progress_tasks = tasks.filter(task_status='2')
    
    context = {
        'all_tasks':all_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks
    }


    return render(request, "mem_template/mem_home_template.html",context)


def member_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    member = TeamMem.objects.get(admin=user)

    context={
        "user": user,
        "member": member
    }
    return render(request, 'mem_template/mem_profile.html', context)


def member_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('member_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = TeamMem.objects.get(admin=customuser.id)
            
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('member_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('member_profile')


def member_view_task(request):
    try:
        team_member = TeamMem.objects.get(admin=request.user)
        assigned_tasks = Task.objects.filter(assigned_member=team_member)
        
    except TeamMem.DoesNotExist:
        assigned_tasks = Task.objects.none()
    context = {
        "tasks": assigned_tasks
    }
    return render(request, "mem_template/member_view_task.html",context)

def member_task_list(request):
    # Get tasks for the assigned member
    team_member = TeamMem.objects.get(admin=request.user)
    tasks = Task.objects.filter(assigned_member=team_member)
    
    # Separate tasks based on their status
    all_tasks = tasks
    completed_tasks = tasks.filter(task_status='3')
    in_progress_tasks = tasks.filter(task_status='2')
    
    context = {
        'all_tasks':all_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks
    }
    return render(request, "mem_template/member_task_list.html", context)



def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskStatusUpdateForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data['task_status']
            task.update_task_status(new_status)

            if new_status == '3':  # Assuming '3' represents the "Completed" status
                # Generate progress report
                progress_report = generate_progress_report(task)
                # Do something with the progress report (e.g., save it, display it, etc.)
                # ...

                return render(request, 'mem_template/task_status_update_success.html', {'progress_report': progress_report})

            return redirect('member_view_task')  # Redirect to the task view

    else:
        form = TaskStatusUpdateForm()

    return render(request, 'mem_template/task_status_update.html', {'form': form, 'task': task})




def generate_progress_report(task):
    # Generate the progress report based on the task's current status and other relevant information
    progress_report = "Progress report for task: {}\n".format(task.task_title)
    progress_report += "Task Description: {}\n".format(task.task_description)
    progress_report += "Task Status: {}\n".format(task.get_task_status_display())
    # Include any other relevant information you want in the progress report

    # Save the progress report in the task's progress_report field
    task.progress_report = progress_report
    task.save()

    return progress_report


def member_projects(request):
    current_member = request.user.teammem
    member_projects = Project.objects.filter(members=current_member)

    context = {
        'member_projects': member_projects,
        'current_member': current_member,
    }

    return render(request, 'mem_template/project_list.html', context)



def get_tasks(request):
    project_id = request.GET.get('project_id')
    project = Project.objects.get(id=project_id)
    members = project.members.all()

    context = {
        'project': project,
        'members': members,
    }
    return render(request, 'mem_template/project_detail.html', context)




def profile(request):
    
    return render(request, "mem_template/profile.html")

def apply_leave1(request):
    emp = CustomUser.objects.get(id=request.user.id)
    leave_data = LeaveReport.objects.filter(emp_id=emp)
    context = {
        "leave_data": leave_data
    }
    return render(request, "mem_template/apply_leave_template.html", context)


def apply_leave_save1(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('apply_leave1')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        emp_obj = CustomUser.objects.get(id=request.user.id)
        try:
            leave_report = LeaveReport(emp_id=emp_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('apply_leave1')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('apply_leave1')


def feedback1(request):
    emp_obj = CustomUser.objects.get(id=request.user.id)
    feedback_data = FeedBack.objects.filter(emp_id=emp_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "mem_template/feedback_template.html", context)


def feedback_save1(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('feedback1')
    else:
        feedback = request.POST.get('feedback_message')
        emp_obj = CustomUser.objects.get(id=request.user.id)

        try:
            add_feedback = FeedBack(emp_id=emp_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('feedback1')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('feedback1')



