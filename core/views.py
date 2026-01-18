from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Avg, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache

from .models import Branch, Semester, Subject, Upload, Rating, Report, PointsLog


# -------------------------
# Points helper
# -------------------------
def add_points(user, action, points):
    PointsLog.objects.create(user=user, action=action, points_change=points)


def get_user_points(user):
    total = PointsLog.objects.filter(user=user).aggregate(total=Sum("points_change"))["total"]
    return total or 0


# -------------------------
# AUTH
# -------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")

        if not username or not password or not confirm:
            messages.error(request, "All fields are required.")
            return redirect("signup")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created. Please login.")
        return redirect("login")

    return render(request, "core/signup.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

        login(request, user)
        return redirect("home")

    return render(request, "core/login.html")

@never_cache
@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------
# HOME + FILTERS
# -------------------------
@login_required
def home(request):
    branches = Branch.objects.all().order_by("name")
    semesters = Semester.objects.all().order_by("number")

    selected_branch = request.GET.get("branch", "")
    selected_semester = request.GET.get("semester", "")
    selected_subject = request.GET.get("subject", "")
    selected_type = request.GET.get("type", "")

    notes = (
        Upload.objects.select_related("subject", "subject__branch", "subject__semester")
        .filter(status__in=["VERIFIED", "UNVERIFIED"])
        .order_by("-created_at")
    )

    if selected_branch:
        notes = notes.filter(subject__branch_id=selected_branch)

    if selected_semester:
        notes = notes.filter(subject__semester_id=selected_semester)

    if selected_subject:
        notes = notes.filter(subject_id=selected_subject)

    if selected_type:
        notes = notes.filter(upload_type=selected_type)

    return render(
        request,
        "core/home.html",
        {
            "branches": branches,
            "semesters": semesters,
            "notes": notes,
            "selected_branch": selected_branch,
            "selected_semester": selected_semester,
            "selected_subject": selected_subject,
            "selected_type": selected_type,
            "user_points": get_user_points(request.user),
        },
    )


# -------------------------
# API: subjects dropdown
# -------------------------
@login_required
def api_subjects(request):
    branch_id = request.GET.get("branch_id")
    semester_id = request.GET.get("semester_id")

    qs = Subject.objects.all()

    if branch_id:
        qs = qs.filter(branch_id=branch_id)

    if semester_id:
        qs = qs.filter(semester_id=semester_id)

    qs = qs.order_by("name")
    data = [{"id": s.id, "name": s.name} for s in qs]
    return JsonResponse(data, safe=False)


# -------------------------
# UPLOAD NOTE
# -------------------------
@login_required
def upload_note(request):
    branches = Branch.objects.all().order_by("name")
    semesters = Semester.objects.all().order_by("number")

    if request.method == "POST":
        branch_id = request.POST.get("branch")
        semester_id = request.POST.get("semester")
        subject_id = request.POST.get("subject")

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        upload_type = request.POST.get("upload_type")
        file = request.FILES.get("file")

        if not (branch_id and semester_id and subject_id and title and upload_type and file):
            messages.error(request, "Please fill all required fields.")
            return redirect("upload_note")

        subject = get_object_or_404(Subject, id=subject_id)

        Upload.objects.create(
            uploader=request.user,
            subject=subject,
            title=title,
            description=description,
            file=file,
            upload_type=upload_type,
            status="UNVERIFIED",
        )

        add_points(request.user, "Uploaded note", 10)
        messages.success(request, "Uploaded successfully! (Unverified)")
        return redirect("my_uploads")

    return render(
        request,
        "core/upload.html",
        {"branches": branches, "semesters": semesters, "user_points": get_user_points(request.user)},
    )


# -------------------------
# VIEW NOTE
# -------------------------
@login_required
def view_note(request, pk):
    note = get_object_or_404(Upload, pk=pk)

    avg_rating = Rating.objects.filter(upload=note).aggregate(avg=Avg("stars"))["avg"]
    rating_count = Rating.objects.filter(upload=note).count()
    my_rating = Rating.objects.filter(upload=note, user=request.user).first()

    return render(
        request,
        "core/view_note.html",
        {
            "note": note,
            "avg_rating": avg_rating,
            "rating_count": rating_count,
            "my_rating": my_rating,
            "user_points": get_user_points(request.user),
        },
    )


# -------------------------
# RATE NOTE
# -------------------------
@require_POST
@login_required
def rate_note(request, pk):
    note = get_object_or_404(Upload, pk=pk)

    stars = request.POST.get("stars")
    try:
        stars = int(stars)
    except:
        messages.error(request, "Invalid rating.")
        return redirect("view_note", pk=pk)

    if stars < 1 or stars > 5:
        messages.error(request, "Rating must be 1 to 5.")
        return redirect("view_note", pk=pk)

    Rating.objects.update_or_create(
        user=request.user,
        upload=note,
        defaults={"stars": stars},
    )

    messages.success(request, "Rating saved.")
    return redirect("view_note", pk=pk)


# -------------------------
# REPORT NOTE
# -------------------------
@require_POST
@login_required
def report_note(request, pk):
    note = get_object_or_404(Upload, pk=pk)
    reason = request.POST.get("reason", "").strip()

    valid_reasons = ["SPAM", "WRONG", "COPYRIGHT", "VULGAR"]

    if reason not in valid_reasons:
        messages.error(request, "Invalid report reason.")
        return redirect("view_note", pk=pk)

    Report.objects.get_or_create(
        reporter=request.user,
        upload=note,
        defaults={"reason": reason},
    )

    messages.success(request, "Report submitted.")
    return redirect("view_note", pk=pk)


# -------------------------
# MY UPLOADS
# -------------------------
@login_required
def my_uploads(request):
    uploads = Upload.objects.filter(uploader=request.user).order_by("-created_at")
    return render(
        request,
        "core/my_uploads.html",
        {"uploads": uploads, "user_points": get_user_points(request.user)},
    )


# -------------------------
# DELETE UPLOAD
# -------------------------
@require_POST
@login_required
def delete_upload(request, pk):
    upload = get_object_or_404(Upload, pk=pk, uploader=request.user)
    upload.delete()
    add_points(request.user, "Deleted upload", -10)
    messages.success(request, "Upload deleted (-10 points).")
    return redirect("my_uploads")


# -------------------------
# LEADERBOARD
# -------------------------
@login_required
def leaderboard(request):
    leaderboard_data = (
        PointsLog.objects.values("user__username")
        .annotate(points=Sum("points_change"))
        .order_by("-points")
    )
    return render(
        request,
        "core/leaderboard.html",
        {"leaderboard_data": leaderboard_data, "user_points": get_user_points(request.user)},
    )


# -------------------------
# ADMIN PANEL
# -------------------------
def is_admin(user):
    return user.is_staff


@user_passes_test(is_admin)
def admin_uploads(request):
    uploads = Upload.objects.select_related("subject", "uploader").order_by("-created_at")
    return render(request, "core/admin_uploads.html", {"uploads": uploads, "user_points": get_user_points(request.user)})


@user_passes_test(is_admin)
def verify_upload(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    upload.status = "VERIFIED"
    upload.save()
    messages.success(request, "Upload verified.")
    return redirect("admin_uploads")


@user_passes_test(is_admin)
def remove_upload(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    upload.status = "REMOVED"
    upload.save()
    messages.success(request, "Upload removed.")
    return redirect("admin_uploads")


@user_passes_test(is_admin)
def admin_reports(request):
    reports = Report.objects.select_related("upload", "reporter").order_by("-created_at")
    return render(request, "core/admin_reports.html", {"reports": reports, "user_points": get_user_points(request.user)})


# -------------------------
# FOOTER PAGES
# -------------------------
@login_required
def privacy_policy(request):
    return render(request, "core/privacy_policy.html", {"user_points": get_user_points(request.user)})


@login_required
def terms(request):
    return render(request, "core/terms.html", {"user_points": get_user_points(request.user)})


@login_required
def disclaimer(request):
    return render(request, "core/disclaimer.html", {"user_points": get_user_points(request.user)})


@login_required
def contact(request):
    return render(request, "core/contact.html", {"user_points": get_user_points(request.user)})