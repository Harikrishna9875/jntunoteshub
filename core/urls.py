from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # auth
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # upload + view
    path("upload/", views.upload_note, name="upload_note"),
    path("view/<int:pk>/", views.view_note, name="view_note"),

    # rating + report
    path("rate/<int:pk>/", views.rate_note, name="rate_note"),
    path("report/<int:pk>/", views.report_note, name="report_note"),

    # my uploads + delete
    path("my-uploads/", views.my_uploads, name="my_uploads"),
    path("delete/<int:pk>/", views.delete_upload, name="delete_upload"),

    # leaderboard
    path("leaderboard/", views.leaderboard, name="leaderboard"),

    # api for dynamic subjects dropdown
    path("api/subjects/", views.api_subjects, name="api_subjects"),
    path("ajax/get-subjects/", views.api_subjects, name="get_subjects"),

    # admin panel
    path("admin-panel/uploads/", views.admin_uploads, name="admin_uploads"),
    path("admin-panel/uploads/<int:pk>/verify/", views.verify_upload, name="verify_upload"),
    path("admin-panel/uploads/<int:pk>/remove/", views.remove_upload, name="remove_upload"),
    path("admin-panel/reports/", views.admin_reports, name="admin_reports"),

    # footer pages
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms/", views.terms, name="terms"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("contact/", views.contact, name="contact"),
]