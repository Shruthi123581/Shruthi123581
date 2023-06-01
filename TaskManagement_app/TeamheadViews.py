from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

###
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .forms import ProjectModelForm, TaskModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.contrib.auth.decorators import login_required
####


from TaskManagement_app.models import CustomUser, TeamHead,TeamMem,Project,Task,LeaveReport,FeedBack

@login_required
def head_home(request):
    
	     
    return render(request, "head_template/head_home_template.html")#context

@login_required
def head_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = TeamHead.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'head_template/head_profile.html', context)

@login_required
def head_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('head_profile')
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

            head = TeamHead.objects.get(admin=customuser.id)
           
            head.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('head_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('head_profile')


def apply_leave(request):
    emp = CustomUser.objects.get(id=request.user.id)
    leave_data = LeaveReport.objects.filter(emp_id=emp)
    context = {
        "leave_data": leave_data
    }
    return render(request, "head_template/apply_leave_template.html", context)


def apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        emp_obj = CustomUser.objects.get(id=request.user.id)
        try:
            leave_report = LeaveReport(emp_id=emp_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('apply_leave')


def feedback(request):
    emp_obj = CustomUser.objects.get(id=request.user.id)
    feedback_data = FeedBack.objects.filter(emp_id=emp_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "head_template/feedback_template.html", context)


def feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('feedback')
    else:
        feedback = request.POST.get('feedback_message')
        emp_obj = CustomUser.objects.get(id=request.user.id)

        try:
            add_feedback = FeedBack(emp_id=emp_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('feedback')



class ProjectList(ListView):
	model = Project
	context_object_name = 'projects'
	queryset = Project.objects.all()
	template_name = 'head_template/project_list.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['projects'] = context ['projects'].filter(owner = self.request.user)
		context ['count_projects'] = context ['projects'].filter(project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		search_input = self.request.GET.get('search-area') or ''
		if search_input:
			context['projects'] = context['projects'].filter(project_title__icontains=search_input)

		context['search_input'] = search_input
		return context


class ProjectDetail(DetailView):
	model = Project
	context_object_name = 'project'
	template_name = 'head_template/project.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()
		

		return context

class ProjectCreate(CreateView):
	model = Project
	form_class = ProjectModelForm
	context_object_name = 'projects'
	template_name = 'head_template/project-create-form.html'
	queryset = Project.objects.all()
	success_url = reverse_lazy('projects')
	

	def form_valid(self, form):
		#form.instance.owner = self.request.user
		project = form.save(commit=False)
		project.owner = self.request.user
		project.save()
		members = form.cleaned_data['members']
		project.members.set(members)


		return super(ProjectCreate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		return context

class ProjectUpdate(UpdateView):
	model = Project
	form_class = ProjectModelForm
	template_name = 'head_template/project-create-form.html'
	success_url = reverse_lazy('projects')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		return context

class DeleteView(DeleteView):
	model = Project
	context_object_name = 'project'
	success_url = reverse_lazy('projects')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		return context


class TaskList(ListView):
	model = Task
	context_object_name = 'tasks'
	template_name = 'head_template/task_list.html'
	queryset = Task.objects.all()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['tasks'] = context ['tasks'].filter(owner = self.request.user)
		context ['count_tasks'] = context ['tasks'].filter(task_complete=False).count()
		context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()

		return context


class TaskDetail(DetailView):
	model = Task
	context_object_name = 'task'
	template_name = 'head_template/task.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		return context


class TaskCreate(CreateView):
	model = Task
	form_class = TaskModelForm
	context_object_name = 'tasks'
	template_name = 'head_template/task_form.html'
	queryset = Task.objects.all()
	success_url = reverse_lazy('tasks')
	
	def get_form(self, *args, **kwargs):
		form = super(TaskCreate, self).get_form(*args, **kwargs)
		form.fields['assigned_member'].queryset = TeamMem.objects.all()
		#form.fields['task_belongs'].queryset = Project.objects.filter(owner=self.request.user)
		#project_id = self.request.GET.get('project_id')

		#if project_id:

		#	project = Project.objects.get(id=project_id)
	#	    form.fields['assigned_member'].queryset = project.members.all()
		return form

	def form_valid(self, form):
		#form =TaskModelForm(self.request.POST, self.request.FILES)
		form.instance.owner = self.request.user
		form.instance.assigned_member = form.cleaned_data['assigned_member']
		project_id = form.cleaned_data['task_belongs'].id if form.cleaned_data['task_belongs'] else None

		if project_id:
			project = Project.objects.get(id=project_id)
			form.instance.task_belongs = project
			
		


		self.object = form.save(commit=False)
		if 'document' in self.request.FILES:
			self.object.document = self.request.FILES['document']

		self.object.save()


		return super(TaskCreate, self).form_valid(form)
	
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		return context


class TaskUpdate(UpdateView):
	model = Task
	form_class = TaskModelForm
	template_name = 'head_template/task_form.html'
	success_url = reverse_lazy('tasks')
	
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context ['count_projects'] = Project.objects.filter(owner=self.request.user, project_complete=False).count()
		context ['count_projects_pending'] = Project.objects.filter(owner=self.request.user, project_status='1').count()
		context ['count_projects_active'] = Project.objects.filter(owner=self.request.user, project_status='2').count()
		context ['count_projects_waiting'] = Project.objects.filter(owner=self.request.user, project_status='3').count()
		context ['count_projects_finished'] = Project.objects.filter(owner=self.request.user, project_status='4').count()
		context ['count_tasks'] = Task.objects.filter(owner=self.request.user, task_complete=False).count()

		return context


