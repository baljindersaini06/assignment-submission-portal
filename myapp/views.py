from .models import User
from friendship.models import Friend, Follow, Block
from django.shortcuts import render, redirect, reverse, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import (
    UserCreateForm, LoginForm, SignUpForm, SetPasswordForm, 
    AssignmentForm, SubmissionForm, RevertForm)
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.views.generic import ListView, TemplateView
from django.contrib.auth.decorators import login_required
from myapp.models import Assignment, Credit, Submission
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError
from django.conf import settings
from friendship.models import Friend, Follow, FriendshipRequest, Block
from django.contrib import messages
# Create your views here.
user_model = User

get_friendship_context_object_name = lambda: getattr(
    settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user"
)
get_friendship_context_object_list_name = lambda: getattr(
    settings, "FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME", "users"
)




def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.role is 1:  
                        return redirect('student')
                    elif user.role is 2:
                        return redirect('teacher')
    
    
    else:
        login_form = LoginForm()
    return render(request, 'myapp/login_base.html', {'login_form': login_form})


# def loginView(request):
#     return render(request, 'myapp/login_base.html')


def signView(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password1'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return reverse('show')
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreateForm()
    return render(request, 'auth/user_form.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponseRedirect(reverse('show'))
    else:
        return HttpResponse('Activation link is invalid!')
        

def contactView(request):
    return render(request, 'myapp/show.html')

def studentView(request):
    return render(request, 'student/studentdash.html')

def teacherView(request):
    return render(request, 'teacher/teacherdash.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.phone_no = form.cleaned_data.get('phone_no')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Student Account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:      
        form = SignUpForm()
        
    return render(request, 'registration/studentsignup.html', {'form': form})



def activates(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('setpassword',args=(uid,)))
    else:
        return HttpResponse('Activation link is invalid!')


def setpassword(request,uid):
    if request.method=='POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=uid)
            password = request.POST.get('password')
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('userlogin')
    else:
        form = SetPasswordForm()
    return render(request,"passwordset.html",{'form':form})

@login_required
def assignView(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return HttpResponse('Assignment has been added successfully')

    else:
        form = AssignmentForm(instance=request.user)
    return render(request, 'teacher/add_assign.html', {'form': form})


def submissionView(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        #form['student'] = submission.objects.get(from_student=request.POST.get('from_student'))
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return HttpResponse('Assignment has been submitted successfully')

    else:
        form = SubmissionForm(instance=request.user)
    return render(request, 'student/submit_assign.html', {'form': form})


def revertView(request):
    if request.method == 'POST':
        form = RevertForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return HttpResponse('Revert has been submitted successfully')

    else:
        form = RevertForm(instance=request.user)
    return render(request, 'teacher/revert_assign.html', {'form': form})


def listingView(request):
    abc = Assignment.objects.filter(student=request.user)

    return render (request, 'student/assign_list.html',{'abc': abc})


def subView(request):
    abc = Submission.objects.filter(to_teacher=request.user)

    return render (request, 'teacher/assign_sub.html',{'abc': abc})

def resultView(request):
    abc = Credit.objects.filter(student_from=request.user)

    return render (request, 'student/assign_result.html', {'abc': abc})



def get_staff(request):
    teach = User.objects.filter(role=2)
    return render(request, 'teacher_list.html', {'teach': teach})


def friendship_add_friend(request, teacher_id):
    xyz = {"teacher_id": teacher_id}

    if request.method == "POST":
        to_user = User.objects.get(pk=teacher_id)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyFriendsError as e:
            xyz["errors"] = ["%s" % e]
        except AlreadyExistsError as e:
            xyz["errors"] = ["%s" % e]
        else:
            return HttpResponse("Request has been sent")

    return render(request, "friendship/friend/add.html", xyz)


def view_friends(request, user_id, template_name="friendship/friend/user_list.html"):
    """ View the friends of a user """
    user = get_object_or_404(user_model, pk=user_id)
    friends = Friend.objects.friends(user)
    return render(request, template_name, {
        get_friendship_context_object_name(): user,
        'friendship_context_object_name': get_friendship_context_object_name(),
        'friends': friends,
    })


def friendship_request_list(request, template_name="friendship/friend/requests_list.html"):
    friendship_requests = Friend.objects.requests(request.user)
    # This shows all friendship requests in the database
    # friendship_requests = FriendshipRequest.objects.filter(rejected__isnull=True)

    return render(request, template_name, {"requests": friendship_requests})


def friendship_requests_detail(request, friendship_request_id, template_name="friendship/friend/request.html"):
    """ View a particular friendship request """
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {"friendship_request": f_request})


def friendship_accept(request, friendship_request_id):
    """ Accept a friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(request.user.friendship_requests_received, id=friendship_request_id)
        f_request.accept()
        return HttpResponse("Request has been accepted")

    return redirect(
        "requests_detail", friendship_request_id=friendship_request_id
    )


def friendship_reject(request, friendship_request_id):
    """ Reject a friendship request """
    if request.method == "POST":
        f_request = get_object_or_404(
            request.user.friendship_requests_received, id=friendship_request_id
        )
        f_request.reject()
        return redirect("teacher")

    return redirect(
        "requests_detail", friendship_request_id=friendship_request_id
    )
