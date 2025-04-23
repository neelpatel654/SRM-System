from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.student_list, name="dashboard"),
    path("students/", views.student_list, name="student_list"),
    path("student", views.my_results, name="my_results"),
    path("student/add/", views.add_student, name="add_student"),
    path("student/update/<int:id>/", views.update_student, name="update_student"),
    path("student/delete/<int:id>/", views.delete_student, name="delete_student"),
    path("profile/", views.student_profile, name="student_profile"),
    path("results/", views.result_list, name="result_list"),
    path("result/add/", views.add_result, name="add_result"),
    path("result/update/<int:id>/", views.update_result, name="update_result"),
    path("result/delete/<int:id>/", views.delete_result, name="delete_result"),
    path("subjects/", views.subject_list, name="subject_list"),
    path("subject/add/", views.add_subject, name="add_subject"),
    path("subject/update/<int:id>/", views.update_subject, name="update_subject"),
    path("subject/delete/<int:id>/", views.delete_subject, name="delete_subject"),
]
