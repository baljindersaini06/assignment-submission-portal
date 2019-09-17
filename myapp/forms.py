from django import forms
from myapp.models import User, Assignment, Submission, Credit
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm



USER_TYPE_CHOICES = (
    (1, 'STUDENT'),
    (2, 'TEACHER'),
)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    role = forms.ChoiceField(widget=forms.Select,choices=USER_TYPE_CHOICES, required=True)
    phone_no = forms.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "phone_no", "role", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        # username = self.cleaned_data.get('username')
        if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
            raise forms.ValidationError('This phone number is already registered.')
        return phone_no

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254,required=True)
    role = forms.ChoiceField(widget=forms.Select,choices=USER_TYPE_CHOICES, required=True)
   
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','phone_no', 'email', 'role')
        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('This email address is already registered.')
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        # username = self.cleaned_data.get('username')
        if phone_no and User.objects.filter(phone_no=phone_no).count() > 0:
            raise forms.ValidationError('This phone number is already registered.')
        return phone_no


class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=30, required=False)
   
    class Meta:
        model = User
        fields = ('password', 'confirm_password')


class AssignmentForm(forms.ModelForm):
	class Meta:
		model = Assignment
		fields = ['teacher','student', 'name','document','deadline']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['assignment_name', 'to_teacher', 'from_student', 'document', 'submission_date']


class RevertForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['assignment', 'teacher_to', 'student_from', 'stars', 'comments']