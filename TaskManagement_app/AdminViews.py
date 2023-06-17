from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.contrib.auth import get_user_model
from TaskManagement_app.models import CustomUser, TeamHead, TeamMem,Project,Task,FeedBack,LeaveReport
from .forms import AddTeamMemForm, EditTeamMemForm


def admin_home(request):
    f_name=request.user.first_name
    l_name=request.user.last_name
    all_Member_count = TeamMem.objects.all().count()
    project_count = Project.objects.all().count()
    task_count = Task.objects.all().count()
    head_count = TeamHead.objects.all().count()
      
    members = TeamMem.objects.all()

    context={
        "fname":f_name,
        "lname":l_name,
        "all_Member_count": all_Member_count,
       "project_count": project_count,
       "task_count":task_count,
        "head_count": head_count,
        
    }
    return render(request, "admin_template/home_content.html", context)

#heads = TeamHead.objects.all()

def add_head(request):
    return render(request, "admin_template/add_head_template.html")


CustomUser = get_user_model()


def add_head_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_head')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_pic')


        try:
            # Create a new CustomUser object
            head = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            # Set additional fields for TeamHead
                      
            head.teamhead.phone = phone
            head.teamhead.address = address
            head.teamhead.gender = gender
            head.teamhead.dob = dob
            #head.teamhead.profile_pic = profile_pic
            if profile_pic:
                head.teamhead.profile_pic = profile_pic

            head.save()
            
            messages.success(request, "Head Added Successfully!")
            return redirect('manage_head')
        except Exception as e:
            # Print the exception message to identify the error
            print(str(e))
            messages.error(request, "Failed to Add Head!")
            return redirect('add_head')



def manage_head(request):
    heads = TeamHead.objects.all()
    context = {
        "heads": heads
    }
    return render(request, "admin_template/manage_head.html", context)


def edit_head(request, head_id):
    head = TeamHead.objects.get(admin=head_id)

    context = {
        "head": head,
        "id": head_id
    }
    return render(request, "admin_template/edit_head_template.html", context)


def edit_head_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        head_id = request.POST.get('head_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_pic')
       
        try:
            # INSERTING into Customuser Model
            user = CustomUser.objects.get(id=head_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            # INSERTING into TeamHead Model
            teamhead = TeamHead.objects.get(admin=head_id)
            teamhead.address = address
            teamhead.phone = phone
            teamhead.gender = gender
            teamhead.dob = dob
            #head_model.profile_pic = profile_pic
            if profile_pic:
                teamhead.profile_pic = profile_pic
            teamhead.save()

            messages.success(request, "Head Updated Successfully.")
            return redirect('/manage_head/')

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_head/'+head_id)



def delete_head(request, head_id):
    head = TeamHead.objects.get(admin=head_id)
    try:
        head.delete()
        messages.success(request, "Head Deleted Successfully.")
        return redirect('manage_head')
    except:
        messages.error(request, "Failed to Delete Head.")
        return redirect('manage_head')



def add_member(request):
    form = AddTeamMemForm()
    context = {
        "form": form
    }
    return render(request, 'admin_template/add_member_template.html', context)


def add_mem_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_member')
    else:
        form = AddTeamMemForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']

            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None


            try:
                user = CustomUser.objects.create_user(username=username,password=password,email=email,
                                                      first_name=first_name,last_name=last_name,user_type=3)

                
                user.teammem.address=address,
                user.teammem.phone=phone,
                user.teammem.profile_pic=profile_pic_url,
                user.teammem.dob=dob,
                user.teammem.gender=gender
                
                user.save()

                messages.success(request, "Member Added Successfully!")
                return redirect('manage_member')
            except:
                messages.error(request, "Failed to Add Member!")
                return redirect('add_member')
        else:
            messages.error(request, "Invalid Form Data")
            return redirect('add_member')



def manage_member(request):
    teammem = TeamMem.objects.all()
    context = {
        "teammem": teammem
    }
    return render(request, 'admin_template/manage_member.html', context)


def edit_member(request, member_id):
   
    teammem =TeamMem.objects.get(admin=member_id)
    form = EditTeamMemForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = teammem.admin.email
    form.fields['username'].initial = teammem.admin.username
    form.fields['first_name'].initial = teammem.admin.first_name
    form.fields['last_name'].initial = teammem.admin.last_name
    form.fields['address'].initial = teammem.address
    form.fields['phone'].initial = teammem.phone
    form.fields['dob'].initial = teammem.dob
    form.fields['gender'].initial = teammem.gender
   
    
    context = {
        "id": member_id,
        "username": teammem.admin.username,
        "form": form
    }
    return render(request, "admin_template/edit_member_template.html", context)


def edit_member_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        member_id = request.session.get('member_id')
        if member_id == None:
            return redirect('/manage_member')

        form = EditTeamMemForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            dob = form.cleaned_data['dob']
            gender = form.cleaned_data['gender']
           

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=member_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Teammem Table
                teammem = TeamMem.objects.get(admin=member_id)
                teammem.address = address
                teammem.phone = phone
                teammem.dob = dob              
                teammem.gender = gender
                if profile_pic_url != None:
                    teammem.profile_pic = profile_pic_url
                teammem.save()
                

                messages.success(request, "member Updated Successfully!")
                return redirect('/manage_member/')
            except:
                messages.success(request, "Failed to Update member.")
                return redirect('/edit_member/'+member_id)
        else:
            return redirect('/edit_member/'+member_id)


def delete_member(request, member_id):
    member= TeamMem.objects.get(admin=member_id)
    try:
        member.delete()
        messages.success(request, "member Deleted Successfully.")
        return redirect('manage_member')
    except:
        messages.error(request, "Failed to Delete member.")
        return redirect('manage_member')


def feedback_message(request):
    feedbacks = FeedBack.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin_template/feedback_template.html', context)


@csrf_exempt
def feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBack.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def leave_view(request):
    leaves = LeaveReport.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'admin_template/leave_view.html', context)


def leave_approve(request, leave_id):
    leave = LeaveReport.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('leave_view')


def leave_reject(request, leave_id):
    leave = LeaveReport.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('leave_view')





@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)








def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'admin_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
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
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def head_profile(request):
    pass


def member_profile(requtest):
    pass



