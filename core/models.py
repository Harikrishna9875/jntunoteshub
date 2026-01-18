from django.db import models
from django.contrib.auth.models import User


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Semester(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Semester {self.number}"


class Subject(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ("branch", "semester", "name")

    def __str__(self):
        return f"{self.branch} - Sem {self.semester.number} - {self.name}"


class Upload(models.Model):
    TYPE_CHOICES = [
        ("NOTES", "Notes"),
        ("SPECTRUM", "Spectrum"),
        ("PYQ", "Previous Year Questions"),
        ("IMP", "Important Questions"),
    ]

    STATUS_CHOICES = [
        ("UNVERIFIED", "Unverified"),
        ("VERIFIED", "Verified"),
        ("REMOVED", "Removed"),
    ]

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    file = models.FileField(upload_to="uploads/")
    upload_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="UNVERIFIED")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_upload_type_display()})"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField()

    class Meta:
        unique_together = ("user", "upload")

    def __str__(self):
        return f"{self.user.username} rated {self.upload.title} ({self.stars})"


class Report(models.Model):
    REASON_CHOICES = [
        ("SPAM", "Spam"),
        ("WRONG", "Wrong Content"),
        ("COPYRIGHT", "Copyright"),
        ("VULGAR", "Vulgar/Abuse"),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reporter", "upload")

    def __str__(self):
        return f"{self.reporter.username} reported {self.upload.title}"


class PointsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    points_change = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.action} ({self.points_change})"
