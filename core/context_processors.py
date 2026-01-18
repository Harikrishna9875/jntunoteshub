from django.db.models import Sum
from .models import PointsLog

def user_points(request):
    if request.user.is_authenticated:
        total = PointsLog.objects.filter(user=request.user).aggregate(
            total=Sum("points_change")
        )["total"] or 0
        return {"user_points": total}
    return {"user_points": 0}
