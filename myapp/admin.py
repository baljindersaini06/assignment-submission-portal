from django.contrib import admin
from myapp.models import User, Assignment, Submission, Credit

# Register your models here.

admin.site.register(User)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Credit)