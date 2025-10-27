"""
Service layer for business logic in the immigration application.
"""
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import TravelDocument, DegmadaForm, KafiilkaForm
from .utils import (
    DocumentValidator, DocumentNumberGenerator,
    DataProcessor, NotificationHelper
)


class TravelDocumentService:
    """Service for handling travel document business logic."""
    
    @staticmethod
    @transaction.atomic
    def create_travel_document(form_data, files=None, user=None):
        """Create a new travel document with validation."""
        # Validate required fields
        required_fields = ['full_name', 'region', 'sponsor_name']
        for field in required_fields:
            if not form_data.get(field):
                raise ValidationError(f"{field} is required")
        
        # Generate document number if not provided
        if not form_data.get('document_number'):
            last_doc = TravelDocument.objects.order_by('-id').first()
            last_id = last_doc.id if last_doc else 0
            form_data['document_number'] = DocumentNumberGenerator.generate_travel_document_number(last_id)
        
        # Create document
        document = TravelDocument.objects.create(**form_data)
        
        if user:
            document.created_by = user
            document.save()
        
        # Send notification
        NotificationHelper.send_document_status_notification(document, 'filled')
        
        return document
    
    @staticmethod
    @transaction.atomic
    def update_document_status(document, new_status):
        """Update document status with validation."""
        old_status = document.status
        
        # Validate status transition
        valid_transitions = {
            'filled': ['approved'],
            'approved': ['printed'],
            'printed': []
        }
        
        if old_status in valid_transitions:
            if new_status not in valid_transitions[old_status]:
                raise ValidationError(
                    f"Cannot transition from {old_status} to {new_status}"
                )
        
        document.status = new_status
        document.updated_at = timezone.now()
        document.save()
        
        # Send notification
        NotificationHelper.send_document_status_notification(document, new_status)
        
        return document
    
    @staticmethod
    def approve_document(document):
        """Approve a travel document."""
        return TravelDocumentService.update_document_status(document, 'approved')
    
    @staticmethod
    def print_document(document):
        """Mark document as printed."""
        return TravelDocumentService.update_document_status(document, 'printed')
    
    @staticmethod
    def get_document_statistics():
        """Get statistics for travel documents."""
        from django.db.models import Count, Q
        from datetime import timedelta
        
        stats = {
            'total': TravelDocument.objects.count(),
            'by_status': dict(
                TravelDocument.objects.values('status').annotate(
                    count=Count('id')
                ).values_list('status', 'count')
            ),
            'recent_30_days': TravelDocument.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=30)
            ).count(),
            'recent_7_days': TravelDocument.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count(),
        }
        
        return stats
    
    @staticmethod
    def search_documents(query, filters=None):
        """Search documents with various filters."""
        qs = TravelDocument.objects.all()
        
        if query:
            qs = qs.filter(
                Q(full_name__icontains=query) |
                Q(document_number__icontains=query) |
                Q(identification_number__icontains=query)
            )
        
        if filters:
            if filters.get('region'):
                qs = qs.filter(region=filters['region'])
            if filters.get('status'):
                qs = qs.filter(status=filters['status'])
            if filters.get('date_from'):
                qs = qs.filter(created_at__gte=filters['date_from'])
            if filters.get('date_to'):
                qs = qs.filter(created_at__lte=filters['date_to'])
        
        return qs.order_by('-created_at')


class FormService:
    """Service for handling form business logic."""
    
    @staticmethod
    @transaction.atomic
    def create_degmada_form(form_data, members_data=None):
        """Create a degmada form with members."""
        # Generate reference if not provided
        if not form_data.get('reference'):
            form_data['reference'] = DocumentNumberGenerator.generate_degmada_reference()
        
        form = DegmadaForm.objects.create(**form_data)
        
        # Add members if provided
        if members_data:
            from .models import DegmadaFormMember
            for member_data in members_data:
                member_data['form'] = form
                DegmadaFormMember.objects.create(**member_data)
        
        return form
    
    @staticmethod
    @transaction.atomic
    def create_kafiilka_form(form_data, members_data=None):
        """Create a kafiilka form with members."""
        # Generate reference if not provided
        if not form_data.get('reference'):
            form_data['reference'] = DocumentNumberGenerator.generate_kafiilka_reference()
        
        form = KafiilkaForm.objects.create(**form_data)
        
        # Add members if provided
        if members_data:
            from .models import KafiilkaFormMember
            for member_data in members_data:
                member_data['form'] = form
                KafiilkaFormMember.objects.create(**member_data)
        
        return form
    
    @staticmethod
    def validate_form_completion(form):
        """Validate that a form is properly filled."""
        errors = []
        
        # Check required fields
        required_fields = ['company_name', 'sponsor_name', 'pledge_name']
        for field in required_fields:
            if not getattr(form, field, None):
                errors.append(f"{field} is required")
        
        # Check if form has members
        if hasattr(form, 'members'):
            if form.members.count() == 0:
                errors.append("Form must have at least one member")
        
        return errors
    
    @staticmethod
    def get_form_statistics():
        """Get statistics about forms."""
        return {
            'total_degmada': DegmadaForm.objects.count(),
            'total_kafiilka': KafiilkaForm.objects.count(),
            'recent_degmada': DegmadaForm.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).count(),
            'recent_kafiilka': KafiilkaForm.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).count(),
        }


class ValidationService:
    """Service for validating immigration data."""
    
    @staticmethod
    def validate_travel_document(data):
        """Validate travel document data."""
        errors = []
        
        # Validate required fields
        required_fields = [
            'full_name', 'mother_name', 'birth_date', 'birth_place',
            'identification_number', 'region', 'sponsor_name'
        ]
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")
        
        # Validate phone number
        if data.get('phone_number'):
            if not DocumentValidator.validate_phone_number(data['phone_number']):
                errors.append("Invalid phone number format")
        
        # Validate ID number
        if data.get('identification_number'):
            if not DocumentValidator.validate_id_number(data['identification_number']):
                errors.append("Invalid identification number format")
        
        # Validate dates
        if data.get('birth_date'):
            age = DocumentValidator.calculate_age(data['birth_date'])
            if age and age < 0:
                errors.append("Birth date cannot be in the future")
            if age and age > 120:
                errors.append("Invalid birth date")
        
        return errors
    
    @staticmethod
    def validate_sponsor_information(data):
        """Validate sponsor information."""
        errors = []
        
        if not data.get('sponsor_name'):
            errors.append("Sponsor name is required")
        
        if not data.get('sponsor_id'):
            errors.append("Sponsor ID is required")
        
        if data.get('sponsor_phone'):
            if not DocumentValidator.validate_phone_number(data['sponsor_phone']):
                errors.append("Invalid sponsor phone number format")
        
        return errors


class AuditService:
    """Service for auditing and tracking changes."""
    
    @staticmethod
    def log_document_change(document, action, user=None, changes=None):
        """Log a change to a document."""
        log_entry = {
            'document_id': document.id,
            'document_number': document.document_number,
            'action': action,
            'timestamp': timezone.now(),
            'user': user.username if user else 'system',
            'changes': changes or {},
        }
        # In a full implementation, this would save to an audit log table
        return log_entry
    
    @staticmethod
    def get_document_history(document):
        """Get history of changes for a document."""
        # Placeholder - in production would query audit log
        return []


class ExportService:
    """Service for exporting data in various formats."""
    
    @staticmethod
    def export_to_excel(documents, filename=None):
        """Export documents to Excel format."""
        from django.http import HttpResponse
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Travel Documents"
        
        # Headers
        headers = [
            'Document Number', 'Full Name', 'Date', 'Region',
            'District', 'Sponsor', 'Status', 'Created At'
        ]
        ws.append(headers)
        
        # Style headers
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center')
        
        # Data rows
        for doc in documents:
            ws.append([
                doc.document_number,
                doc.full_name,
                doc.date.strftime('%Y-%m-%d') if doc.date else '',
                doc.region,
                doc.district,
                doc.sponsor_name,
                doc.get_status_display(),
                doc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])
        
        # Auto-adjust column widths
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = filename or f'travel_documents_{timezone.now().strftime("%Y%m%d")}.xlsx'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response

