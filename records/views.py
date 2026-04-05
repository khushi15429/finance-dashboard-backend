from rest_framework              import generics, status, filters
from rest_framework.response     import Response
from rest_framework.views        import APIView
from rest_framework.permissions  import IsAuthenticated
from django.utils                import timezone
from django.shortcuts            import get_object_or_404

from .models       import FinancialRecord
from .serializers  import FinancialRecordSerializer, FinancialRecordUpdateSerializer
from users.permissions import IsAdmin, IsAnalystOrAdmin


class FinancialRecordListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/records/        — analyst & admin (with filters)
    POST /api/records/        — admin only
    """
    serializer_class = FinancialRecordSerializer
    filter_backends  = [filters.OrderingFilter]
    ordering_fields  = ['date', 'amount', 'created_at']
    ordering         = ['-date']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAnalystOrAdmin()]

    def get_queryset(self):
        # base queryset — exclude soft deleted records
        qs = FinancialRecord.objects.filter(deleted_at__isnull=True)

        # --- filtering ---
        record_type = self.request.query_params.get('type')
        category    = self.request.query_params.get('category')
        date_from   = self.request.query_params.get('date_from')
        date_to     = self.request.query_params.get('date_to')

        if record_type:
            qs = qs.filter(type=record_type)
        if category:
            qs = qs.filter(category=category)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)

        return qs

    def perform_create(self, serializer):
        # automatically assign logged-in user as owner
        serializer.save(user=self.request.user)


class FinancialRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/records/<id>/  — analyst & admin
    PATCH  /api/records/<id>/  — admin only
    DELETE /api/records/<id>/  — admin only (soft delete)
    """
    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT', 'DELETE'):
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated(), IsAnalystOrAdmin()]

    def get_queryset(self):
        return FinancialRecord.objects.filter(deleted_at__isnull=True)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return FinancialRecordUpdateSerializer
        return FinancialRecordSerializer

    def destroy(self, request, *args, **kwargs):
        # soft delete — set deleted_at instead of removing the row
        record = self.get_object()
        record.deleted_at = timezone.now()
        record.save()
        return Response(
            {'message': 'Record deleted successfully.'},
            status=status.HTTP_200_OK
        )