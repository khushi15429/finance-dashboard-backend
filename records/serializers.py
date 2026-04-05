from rest_framework import serializers
from .models import FinancialRecord, TransactionType, Category


class FinancialRecordSerializer(serializers.ModelSerializer):
    """Full serializer — used for create and responses."""
    user = serializers.StringRelatedField(read_only=True)  # shows email

    class Meta:
        model  = FinancialRecord
        fields = (
            'id', 'user', 'amount', 'type',
            'category', 'date', 'notes',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def validate_type(self, value):
        if value not in TransactionType.values:
            raise serializers.ValidationError(
                f'Type must be one of: {TransactionType.values}'
            )
        return value

    def validate_category(self, value):
        if value not in Category.values:
            raise serializers.ValidationError(
                f'Category must be one of: {Category.values}'
            )
        return value


class FinancialRecordUpdateSerializer(serializers.ModelSerializer):
    """Used for partial updates — all fields optional."""

    class Meta:
        model  = FinancialRecord
        fields = ('amount', 'type', 'category', 'date', 'notes')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value