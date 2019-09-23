from django.urls import path
from django.conf.urls import url
from . import views 
from friendship.views import friendship_add_friend, view_friends
from .views import MessageView


urlpatterns=[
    #path('accounts/login', views.loginView, name = 'accounts'),
    path('userlog', views.signView, name='user'),
    path('signup',views.signup,name='signup'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('setpassword/<int:uid>',views.setpassword,name='setpassword'),
    path('show', views.contactView, name='show'),
    path('studentdashbord', views.studentView, name='student'),
    path('teacherdashboard', views.teacherView, name='teacher'),
    path('', views.user_login, name='userlogin'),
    path('activates/<uidb64>/<token>/',views.activates, name='activates'),
    path('teacher/assign/<int:user_id>', views.assignView, name='teacher/assign'),
    path('student/submit/<int:teacher_id>/<int:ass_id>', views.submissionView, name='student/submit'),
    path('teacher/revert', views.revertView, name='teacher/revert'),
    path('student/listing', views.listingView, name='student/listing'),
    path('teacher/sub', views.subView, name='teacher/sub'),
    path('student/result', views.resultView, name='student/result'),
    path('friendadd/<int:teacher_id>', views.friendship_add_friend, name='friend'),
    path('list', views.get_staff, name='list'),
    path('requests', views.friendship_request_list, name='requests'),
    path('requests_detail/<int:friendship_request_id>', views.friendship_requests_detail, name='requests_detail'),
    path('accept/<int:friendship_request_id>', views.friendship_accept, name='accept'),
    path('decline/<int:friendship_request_id>', views.friendship_reject, name='decline'),
    path('friends/<int:user_id>', views.view_friends, name='friends'),
    path('studentfriends/<int:user_id>', views.student_friends, name='studentfriends'),
    path('text/<int:user_id>', views.view_message, name='text'),
    path('sendmsg/<int:user_id>', views.create_message, name='sendmsg'),
    path('addmessage',MessageView.as_view(), name='addmessage'),
    path('chat/<int:user_id>', views.message_post, name='chat'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('teacherchat/<int:user_id>', views.message_teacher, name='teacherchat'),
]