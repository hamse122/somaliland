"""
Custom filters for the immigration application.
"""
import django_filters
from django.db.models import Q
from .models import TravelDocument, DegmadaForm, KafiilkaForm


class TravelDocumentFilter(django_filters.FilterSet):
    """Filter for travel documents."""
    
    document_number = django_filters.CharFilter(lookup_expr='icontains')
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    identification_number = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')
    
    region = django_filters.CharFilter(lookup_expr='iexact')
    district = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.ChoiceFilter(
        choices=TravelDocument.STATUS_CHOICES,
        lookup_expr='iexact'
    )
    
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    created_from = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_to = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    filled_from = django_filters.DateFilter(
        field_name='filled_date',
        lookup_expr='gte'
    )
    filled_to = django_filters.DateFilter(
        field_name='filled_date',
        lookup_expr='lte'
    )
    
    has_notayo = django_filters.BooleanFilter()
    has_sponsor_id = django_filters.BooleanFilter()
    has_damaged_id = django_filters.BooleanFilter()
    has_company_license = django_filters.BooleanFilter()
    has_other_documents = django_filters.BooleanFilter()
    
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = TravelDocument
        fields = [
            'document_number', 'full_name', 'identification_number',
            'phone_number', 'region', 'district', 'status',
            'date_from', 'date_to', 'created_from', 'created_to',
            'filled_from', 'filled_to', 'has_notayo', 'has_sponsor_id',
            'has_damaged_id', 'has_company_license', 'has_other_documents',
            'search'
        ]
    
    def filter_search(self, queryset, name, value):
        """Search across multiple fields."""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(full_name__icontains=value) |
            Q(document_number__icontains=value) |
            Q(identification_number__icontains=value) |
            Q(phone_number__icontains=value) |
            Q(sponsor_name__icontains=value) |
            Q(region__icontains=value) |
            Q(district__icontains=value)
        )
    
    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('date', 'date'),
            ('full_name', 'full_name'),
            ('document_number', 'document_number'),
            ('status', 'status'),
        )
    )


class DegmadaFormFilter(django_filters.FilterSet):
    """Filter for degmada forms."""
    
    reference = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    sponsor_name = django_filters.CharFilter(lookup_expr='icontains')
    
    gobolka = django_filters.CharFilter(lookup_expr='iexact')
    degmada = django_filters.CharFilter(lookup_expr='iexact')
    company_region = django_filters.CharFilter(lookup_expr='iexact')
    
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    created_from = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_to = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = DegmadaForm
        fields = [
            'reference', 'company_name', 'sponsor_name',
            'gobolka', 'degmada', 'company_region',
            'date_from', 'date_to', 'created_from', 'created_to',
            'search'
        ]
    
    def filter_search(self, queryset, name, value):
        """Search across multiple fields."""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(reference__icontains=value) |
            Q(company_name__icontains=value) |
            Q(sponsor_name__icontains=value) |
            Q(gobolka__icontains=value) |
            Q(degmada__icontains=value)
        )
    
    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('date', 'date'),
            ('company_name', 'company_name'),
            ('reference', 'reference'),
        )
    )


class KafiilkaFormFilter(django_filters.FilterSet):
    """Filter for kafiilka forms."""
    
    reference = django_filters.CharFilter(lookup_expr='icontains')
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    sponsor_name = django_filters.CharFilter(lookup_expr='icontains')
    
    gobolka = django_filters.CharFilter(lookup_expr='iexact')
    degmada = django_filters.CharFilter(lookup_expr='iexact')
    company_region = django_filters.CharFilter(lookup_expr='iexact')
    
    sponsor_type = django_filters.ChoiceFilter(
        choices=[
            ('SHASI', 'Individual'),
            ('WADAR', 'Group')
        ]
    )
    
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    
    created_from = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_to = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = KafiilkaForm
        fields = [
            'reference', 'company_name', 'sponsor_name',
            'gobolka', 'degmada', 'company_region', 'sponsor_type',
            'date_from', 'date_to', 'created_from', 'created_to',
            'search'
        ]
    
    def filter_search(self, queryset, name, value):
        """Search across multiple fields."""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(reference__icontains=value) |
            Q(company_name__icontains=value) |
            Q(sponsor_name__icontains=value) |
            Q(gobolka__icontains=value) |
            Q(degmada__icontains=value)
        )
    
    order_by = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('date', 'date'),
            ('company_name', 'company_name'),
            ('reference', 'reference'),
        )
    )

