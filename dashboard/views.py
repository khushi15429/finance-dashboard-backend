from rest_framework.views     import APIView
from rest_framework.response  import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models         import Sum, Count, Q
from django.db.models.functions import TruncMonth, TruncWeek
from django.utils             import timezone
from datetime                 import timedelta

from records.models    import FinancialRecord, TransactionType
from users.permissions import IsAnalystOrAdmin, IsViewer


class SummaryView(APIView):
    """
    GET /api/dashboard/summary/
    Returns total income, expenses and net balance.
    Accessible by all authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = FinancialRecord.objects.filter(deleted_at__isnull=True)

        total_income = qs.filter(
            type=TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expenses = qs.filter(
            type=TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or 0

        net_balance = total_income - total_expenses

        return Response({
            'total_income':   float(total_income),
            'total_expenses': float(total_expenses),
            'net_balance':    float(net_balance),
        })


class CategoryBreakdownView(APIView):
    """
    GET /api/dashboard/categories/
    Returns total amount grouped by category.
    Accessible by analyst and admin.
    """
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        qs = FinancialRecord.objects.filter(deleted_at__isnull=True)

        # optional filter by type
        record_type = request.query_params.get('type')
        if record_type:
            qs = qs.filter(type=record_type)

        breakdown = (
            qs.values('category', 'type')
              .annotate(
                  total=Sum('amount'),
                  count=Count('id')
              )
              .order_by('-total')
        )

        return Response({
            'filters':   {'type': record_type or 'all'},
            'breakdown': list(breakdown),
        })


class MonthlyTrendsView(APIView):
    """
    GET /api/dashboard/trends/monthly/
    Returns income and expenses grouped by month.
    Accessible by analyst and admin.
    """
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        qs = FinancialRecord.objects.filter(deleted_at__isnull=True)

        # optional — last N months filter
        months = int(request.query_params.get('months', 6))
        since  = timezone.now().date() - timedelta(days=30 * months)
        qs     = qs.filter(date__gte=since)

        trends = (
            qs.annotate(month=TruncMonth('date'))
              .values('month', 'type')
              .annotate(total=Sum('amount'))
              .order_by('month')
        )

        # structure the data month by month
        result = {}
        for entry in trends:
            month_key = entry['month'].strftime('%Y-%m')
            if month_key not in result:
                result[month_key] = {
                    'month':   month_key,
                    'income':  0,
                    'expense': 0,
                }
            if entry['type'] == TransactionType.INCOME:
                result[month_key]['income'] = float(entry['total'])
            else:
                result[month_key]['expense'] = float(entry['total'])

        return Response({
            'period_months': months,
            'trends':        list(result.values()),
        })


class WeeklyTrendsView(APIView):
    """
    GET /api/dashboard/trends/weekly/
    Returns income and expenses grouped by week.
    Accessible by analyst and admin.
    """
    permission_classes = [IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        qs = FinancialRecord.objects.filter(deleted_at__isnull=True)

        # last 8 weeks by default
        weeks = int(request.query_params.get('weeks', 8))
        since = timezone.now().date() - timedelta(weeks=weeks)
        qs    = qs.filter(date__gte=since)

        trends = (
            qs.annotate(week=TruncWeek('date'))
              .values('week', 'type')
              .annotate(total=Sum('amount'))
              .order_by('week')
        )

        result = {}
        for entry in trends:
            week_key = entry['week'].strftime('%Y-%m-%d')
            if week_key not in result:
                result[week_key] = {
                    'week':    week_key,
                    'income':  0,
                    'expense': 0,
                }
            if entry['type'] == TransactionType.INCOME:
                result[week_key]['income'] = float(entry['total'])
            else:
                result[week_key]['expense'] = float(entry['total'])

        return Response({
            'period_weeks': weeks,
            'trends':       list(result.values()),
        })


class RecentActivityView(APIView):
    """
    GET /api/dashboard/recent/
    Returns the 10 most recent transactions.
    Accessible by all authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from records.serializers import FinancialRecordSerializer

        limit   = int(request.query_params.get('limit', 10))
        records = FinancialRecord.objects.filter(
                      deleted_at__isnull=True
                  ).order_by('-date', '-created_at')[:limit]

        serializer = FinancialRecordSerializer(records, many=True)
        return Response({
            'count':   len(serializer.data),
            'records': serializer.data,
        })


class FullDashboardView(APIView):
    """
    GET /api/dashboard/
    Returns everything in one single call —
    summary + categories + recent activity.
    Accessible by all authenticated users.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from records.serializers import FinancialRecordSerializer

        qs = FinancialRecord.objects.filter(deleted_at__isnull=True)

        # --- summary ---
        total_income = qs.filter(
            type=TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expenses = qs.filter(
            type=TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or 0

        # --- category breakdown ---
        breakdown = (
            qs.values('category', 'type')
              .annotate(total=Sum('amount'), count=Count('id'))
              .order_by('-total')
        )

        # --- recent 5 transactions ---
        recent = qs.order_by('-date', '-created_at')[:5]
        recent_serializer = FinancialRecordSerializer(recent, many=True)

        return Response({
            'summary': {
                'total_income':   float(total_income),
                'total_expenses': float(total_expenses),
                'net_balance':    float(total_income - total_expenses),
            },
            'category_breakdown': list(breakdown),
            'recent_activity':    recent_serializer.data,
        })