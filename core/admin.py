from django.contrib import admin
from .models import Branch, Semester, Subject, Upload, Rating, Report, PointsLog


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ["number"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["name", "branch", "semester"]
    list_filter = ["branch", "semester"]
    search_fields = ["name"]


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ["title", "upload_type", "status", "subject", "uploader", "created_at"]
    list_filter = ["upload_type", "status", "subject__branch", "subject__semester"]
    search_fields = ["title", "description", "uploader__username"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["user", "upload", "stars"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["reporter", "upload", "reason", "created_at"]
    list_filter = ["reason", "created_at"]


@admin.register(PointsLog)
class PointsLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "points_change", "created_at"]
    list_filter = ["action", "created_at"]
