from django import forms 
from django.forms import Form
#from TaskManagement_app.models import SessionYearModel
from .models import Project, Task,TeamMem

from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = "date"


class AddTeamMemForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
   # address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    #try:
    #    courses = Courses.objects.all()
    #    course_list = []
    #    for course in courses:
    #        single_course = (course.id, course.course_name)
    #        course_list.append(single_course)
    #except:
    #    course_list = []
    

    #For Displaying Session Years
   # try:
   #    session_years = SessionYearModel.objects.all()
   #     session_year_list = []
   #     for session_year in session_years:
   #         single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
   #         session_year_list.append(single_session_year)
            
   # except:
   #     session_year_list = []
    
    #gender_list = (
    #    ('Male','Male'),
    #    ('Female','Female')
    #)
    
    #course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    #gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    #session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    #profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))



class EditTeamMemForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    #address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    #try:
    #    courses = Courses.objects.all()
    #    course_list = []
    #    for course in courses:
    #        single_course = (course.id, course.course_name)
    #        course_list.append(single_course)
    #except:
    #    course_list = []

    #For Displaying Session Years
    #try:
    #    session_years = SessionYearModel.objects.all()
    #    session_year_list = []
    #    for session_year in session_years:
    #        single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
    #        session_year_list.append(single_session_year)
            
    #except:
    #    session_year_list = []

    
    #gender_list = (
    #    ('Male','Male'),
    #    ('Female','Female')
    #)
    
    #course_id = forms.ChoiceField(label="Course", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    #gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    #session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    #profile_pic = forms.FileField(label="Profile Pic", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))




   

class ProjectModelForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['project_title', 'project_status', 'project_intro', 'project_description', 'project_due_date', 'project_complete','members']
		
		members = forms.ModelMultipleChoiceField(
                         queryset=TeamMem.objects.all()
                       )
		widgets = {
			'project_due_date': DateInput(),
	        
		}

class TaskModelForm(ModelForm):
    
    assigned_member = forms.ModelChoiceField(queryset=TeamMem.objects.all())
    

    class Meta:
        model = Task
        fields = ['task_title', 'task_belongs', 'task_description','document','assigned_member', 'task_due_date','task_status','task_important', 'task_complete']
        widgets = {
			'task_due_date': DateInput()
		}

    #def __init__(self, *args, **kwargs):
    #     super(TaskModelForm, self).__init__(*args, **kwargs)
    #     self.fields['assigned_member'].queryset = TeamMem.objects.none()
     #    if 'task_belongs' in self.data:
     #       try:
     #            project_id = int(self.data.get('task_belongs'))
     #            project = Project.objects.get(id=project_id)
     #            self.fields['assigned_member'].queryset = project.members.all()
     #       except (ValueError, TypeError):
     #            pass      
     #    elif self.instance.pk:
     #         project = self.instance.task_belongs
     #         self.fields['assigned_member'].queryset = project.members.all()
 
		
class TaskStatusUpdateForm(forms.Form):
    task_status = forms.ChoiceField(choices=Task.CHOICES)

    
    
    
    
    
    