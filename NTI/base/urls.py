from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("status/", views.status, name='status'),
    path('student-account/', views.student_account, name='student_account'),
    path("teacher-account/", views.teacher_account, name='teacher-account'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('teacher/', views.teacher_login, name='teacher'),
    path('signout/', views.signout, name='signout'),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
