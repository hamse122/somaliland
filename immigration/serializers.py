"""
Serializers for the immigration application API.
"""
from rest_framework import serializers
from .models import (
    TravelDocument, TravelDocumentChild,
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember
)
from django.contrib.auth import get_user_model

User = get_user_model()


class TravelDocumentChildSerializer(serializers.ModelSerializer):
    """Serializer for travel document children."""
    
    class Meta:
        model = TravelDocumentChild
        fields = [
            'id', 'name', 'birth_date', 'birth_place', 'photo',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TravelDocumentSerializer(serializers.ModelSerializer):
    """Serializer for travel documents."""
    children = TravelDocumentChildSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    
    class Meta:
        model = TravelDocument
        fields = [
            'id', 'document_number', 'region_office', 'date',
            'full_name', 'mother_name', 'birth_date', 'birth_place',
            'identification_number', 'region', 'district', 'workplace',
            'sponsor_name', 'citizen_card', 'phone_number', 'nationality',
            'job_type', 'license_number', 'contact_number',
            'filled_date', 'has_notayo', 'has_sponsor_id', 'has_damaged_id',
            'has_company_license', 'has_other_documents',
            'immigration_officer_notes', 'status', 'card_number',
            'officer_signature', 'photo', 'children', 'created_at',
            'updated_at', 'created_by', 'created_by_username', 'status_display'
        ]
        read_only_fields = [
            'id', 'document_number', 'created_at', 'updated_at',
            'created_by', 'created_by_username', 'status_display'
        ]


class TravelDocumentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating travel documents."""
    children = TravelDocumentChildSerializer(many=True, required=False)
    
    class Meta:
        model = TravelDocument
        fields = [
            'region_office', 'date', 'full_name', 'mother_name',
            'birth_date', 'birth_place', 'identification_number',
            'region', 'district', 'workplace', 'sponsor_name',
            'citizen_card', 'phone_number', 'nationality', 'job_type',
            'license_number', 'contact_number', 'filled_date',
            'has_notayo', 'has_sponsor_id', 'has_damaged_id',
            'has_company_license', 'has_other_documents',
            'immigration_officer_notes', 'status', 'card_number',
            'officer_signature', 'photo', 'children'
        ]
    
    def create(self, validated_data):
        children_data = validated_data.pop('children', [])
        document = TravelDocument.objects.create(**validated_data)
        
        for child_data in children_data:
            TravelDocumentChild.objects.create(document=document, **child_data)
        
        return document


class TravelDocumentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating travel documents."""
    children = TravelDocumentChildSerializer(many=True, required=False)
    
    class Meta:
        model = TravelDocument
        fields = [
            'region_office', 'date', 'full_name', 'mother_name',
            'birth_date', 'birth_place', 'identification_number',
            'region', 'district', 'workplace', 'sponsor_name',
            'citizen_card', 'phone_number', 'nationality', 'job_type',
            'license_number', 'contact_number', 'filled_date',
            'has_notayo', 'has_sponsor_id', 'has_damaged_id',
            'has_company_license', 'has_other_documents',
            'immigration_officer_notes', 'status', 'card_number',
            'officer_signature', 'photo', 'children'
        ]
    
    def update(self, instance, validated_data):
        children_data = validated_data.pop('children', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        if children_data is not None:
            # Clear existing children
            instance.children.all().delete()
            
            # Create new children
            for child_data in children_data:
                TravelDocumentChild.objects.create(document=instance, **child_data)
        
        return instance


class DegmadaFormMemberSerializer(serializers.ModelSerializer):
    """Serializer for degmada form members."""
    
    class Meta:
        model = DegmadaFormMember
        fields = [
            'id', 'name', 'nationality', 'birth_date', 'phone',
            'id_number', 'photo'
        ]


class DegmadaFormSerializer(serializers.ModelSerializer):
    """Serializer for degmada forms."""
    members = DegmadaFormMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = DegmadaForm
        fields = [
            'id', 'reference', 'date', 'gobolka', 'degmada',
            'company_name', 'company_license', 'establishment_period',
            'working_employees', 'company_region', 'company_district',
            'sponsor_name', 'sponsor_id', 'sponsor_phone', 'sponsor_contact',
            'sponsor_address', 'pledge_name', 'pledge_signature',
            'district_leader_name', 'district_leader_signature',
            'filled_date', 'attachment_types', 'special_notes',
            'created_at', 'updated_at', 'members'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class KafiilkaFormMemberSerializer(serializers.ModelSerializer):
    """Serializer for kafiilka form members."""
    
    class Meta:
        model = KafiilkaFormMember
        fields = [
            'id', 'name', 'nationality', 'birth_date', 'phone',
            'id_number', 'photo'
        ]


class KafiilkaFormSerializer(serializers.ModelSerializer):
    """Serializer for kafiilka forms."""
    members = KafiilkaFormMemberSerializer(many=True, read_only=True)
    sponsor_type_display = serializers.CharField(
        source='get_sponsor_type_display',
        read_only=True
    )
    
    class Meta:
        model = KafiilkaForm
        fields = [
            'id', 'reference', 'date', 'gobolka', 'degmada',
            'company_name', 'company_license', 'establishment_period',
            'working_employees', 'company_region', 'company_district',
            'sponsor_type', 'sponsor_name', 'sponsor_id', 'sponsor_phone',
            'sponsor_contact', 'sponsor_address', 'pledge_name',
            'pledge_signature', 'district_leader_name',
            'district_leader_signature', 'filled_date', 'attachment_types',
            'special_notes', 'created_at', 'updated_at', 'members',
            'sponsor_type_display'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'sponsor_type_display']


class StatisticsSerializer(serializers.Serializer):
    """Serializer for statistics data."""
    total_documents = serializers.IntegerField()
    approved_documents = serializers.IntegerField()
    filled_documents = serializers.IntegerField()
    printed_documents = serializers.IntegerField()
    recent_documents = serializers.IntegerField()
    
    total_degmada = serializers.IntegerField()
    total_kafiilka = serializers.IntegerField()
    
    recent_degmada = serializers.IntegerField()
    recent_kafiilka = serializers.IntegerField()


class DocumentSearchSerializer(serializers.Serializer):
    """Serializer for document search parameters."""
    query = serializers.CharField(required=False, allow_blank=True)
    region = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(required=False, allow_blank=True)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    sort_by = serializers.CharField(required=False, default='-created_at')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class AuditLogSerializer(serializers.Serializer):
    """Serializer for audit log entries."""
    document_id = serializers.IntegerField()
    document_number = serializers.CharField()
    action = serializers.CharField()
    timestamp = serializers.DateTimeField()
    user = serializers.CharField()
    changes = serializers.DictField()


class ExportRequestSerializer(serializers.Serializer):
    """Serializer for export requests."""
    format = serializers.ChoiceField(
        choices=['csv', 'excel', 'pdf', 'json'],
        default='excel'
    )
    filters = DocumentSearchSerializer(required=False)
    include_children = serializers.BooleanField(default=True)
    include_photos = serializers.BooleanField(default=False)


class BulkOperationSerializer(serializers.Serializer):
    """Serializer for bulk operations."""
    document_ids = serializers.ListField(
        child=serializers.IntegerField()
    )
    operation = serializers.ChoiceField(
        choices=['approve', 'print', 'delete', 'export']
    )

