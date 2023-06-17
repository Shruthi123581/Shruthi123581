from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "TeamHead"), (3, "TeamMem"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
   

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    
)


class AdminHR(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TeamHead(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=20,null=True)
    profile_pic = models.ImageField(upload_to="profile_pics",null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class TeamMem(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=20,null=True)
    profile_pic = models.FileField(upload_to='profile_pics/',null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
         return str(self.admin.first_name)



class Project(models.Model):
        CHOICES = [
		('1', 'Pending'),
		('2', 'Active'),
		('3', 'Waiting'),
		('4', 'Invoiced')
		]
        
        owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = True, blank = True)
        project_title = models.CharField(max_length=200,null=True, blank=True)
        project_intro = models.CharField(max_length=300,null=True, blank=True)
        project_description = models.TextField(blank=True, null=True)
        project_status = models.CharField(choices = CHOICES, max_length=200, null=True, blank=True)
        
        project_complete = models.BooleanField(default=False)
        project_create = models.DateTimeField(auto_now_add=True)
        project_due_date = models.DateField(auto_now_add=False, null=True, blank=False)
        members = models.ManyToManyField(TeamMem,related_name='projects')
        

        def is_due_date(self):
             return date.today() < self.project_due_date
        
        def __str__(self):
            return str(self.project_title)
        
        class Meta:
            ordering = ['project_complete']
     
	
                
                

class Task(models.Model):
    CHOICES = [
		('1', 'New'),
		('2', 'In Progress'),
		('3', 'Completed'),
		]
    def get_task_status_display(self):
        return dict(self.CHOICES).get(self.task_status)
    
    def update_task_status(self, new_status):
        self.task_status = new_status
        self.save()
    
    owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE, null = True, blank = True)
    task_title = models.CharField(max_length=200,null=True, blank=True)
    task_belongs = models.ForeignKey(Project, on_delete = models.CASCADE, null = True, blank = True)
    task_description = models.CharField(max_length=300, null=True, blank=True) 
    document = models.FileField(upload_to='documents/')
    task_due_date = models.DateField(auto_now_add=False,null=True, blank=False)
    task_status = models.CharField(choices = CHOICES, max_length=200, null=True, blank=True)
    task_important = models.BooleanField(default=False)
    task_complete = models.BooleanField(default=False)
    task_create = models.DateTimeField(auto_now_add=True)
    assigned_member = models.ForeignKey(TeamMem, on_delete=models.CASCADE)
    progress_report = models.TextField(blank=True)

	#vždy uvést datum u tasku
    def is_task_due_date(self):
        return date.today() < self.task_due_date
    
    def __str__(self):
        return str(self.task_title)
    
    class Meta:
         ordering = ['task_complete']



class LeaveReport(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class FeedBack(models.Model):
    id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()










    #Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHR.objects.create(admin=instance)
        if instance.user_type == 2:
            TeamHead.objects.create(admin=instance)
        if instance.user_type == 3:
            TeamMem.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhr.save()
    if instance.user_type == 2:
        instance.teamhead.save()
    if instance.user_type == 3:
        instance.teammem.save()
    