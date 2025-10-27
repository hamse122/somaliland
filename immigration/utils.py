"""
Utility functions for the immigration application.
"""
import re
from datetime import date, datetime
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class DocumentValidator:
    """Validates various document types and fields."""
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate phone number format."""
        if not phone:
            return False
        # Allow international and local formats
        pattern = r'^(\+252|0)?[6-7][0-9]{7,8}$'
        return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))
    
    @staticmethod
    def validate_id_number(id_number):
        """Validate Somaliland ID number."""
        if not id_number:
            return False
        # Basic validation - should be alphanumeric and reasonable length
        pattern = r'^[A-Z0-9]{5,20}$'
        return bool(re.match(pattern, id_number.upper()))
    
    @staticmethod
    def validate_date_range(start_date, end_date):
        """Validate that start_date is before end_date."""
        if start_date and end_date:
            return start_date <= end_date
        return True
    
    @staticmethod
    def calculate_age(birth_date):
        """Calculate age from birth date."""
        if not birth_date:
            return None
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    @staticmethod
    def is_adult(birth_date):
        """Check if person is 18 years or older."""
        age = DocumentValidator.calculate_age(birth_date)
        return age >= 18 if age else False


class DocumentNumberGenerator:
    """Generate unique document numbers for various document types."""
    
    @staticmethod
    def generate_travel_document_number(last_id=None):
        """Generate a travel document number."""
        if last_id is None:
            from .models import TravelDocument
            last_doc = TravelDocument.objects.order_by('-id').first()
            last_id = last_doc.id if last_doc else 0
        
        return f"TD-{str(last_id + 1).zfill(5)}"
    
    @staticmethod
    def generate_degmada_reference():
        """Generate a degmada form reference."""
        from django.utils import timezone
        now = timezone.now()
        return f"DEG-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"
    
    @staticmethod
    def generate_kafiilka_reference():
        """Generate a kafiilka form reference."""
        from django.utils import timezone
        now = timezone.now()
        return f"KAF-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"


class DataProcessor:
    """Process and transform data for various purposes."""
    
    @staticmethod
    def clean_phone_number(phone):
        """Clean and normalize phone number."""
        if not phone:
            return ''
        # Remove spaces, dashes, and convert to standard format
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return cleaned
    
    @staticmethod
    def format_identification_number(id_number):
        """Format identification number with proper casing."""
        if not id_number:
            return ''
        return id_number.upper().strip()
    
    @staticmethod
    def extract_name_parts(full_name):
        """Extract first name, last name from full name."""
        if not full_name:
            return {'first_name': '', 'last_name': ''}
        
        parts = full_name.strip().split()
        if len(parts) >= 2:
            return {
                'first_name': parts[0],
                'last_name': ' '.join(parts[1:])
            }
        return {
            'first_name': full_name,
            'last_name': ''
        }
    
    @staticmethod
    def validate_required_documents(document):
        """Validate that all required documents are present."""
        required_docs = {
            'notayo': document.has_notayo if hasattr(document, 'has_notayo') else False,
            'sponsor_id': document.has_sponsor_id if hasattr(document, 'has_sponsor_id') else False,
            'damaged_id': document.has_damaged_id if hasattr(document, 'has_damaged_id') else False,
            'company_license': document.has_company_license if hasattr(document, 'has_company_license') else False,
        }
        return required_docs


class ReportGenerator:
    """Generate various reports from immigration data."""
    
    @staticmethod
    def get_statistics():
        """Get general statistics about immigration documents."""
        from .models import TravelDocument, DegmadaForm, KafiilkaForm
        
        stats = {
            'total_travel_documents': TravelDocument.objects.count(),
            'approved_documents': TravelDocument.objects.filter(status='approved').count(),
            'filled_documents': TravelDocument.objects.filter(status='filled').count(),
            'printed_documents': TravelDocument.objects.filter(status='printed').count(),
            'total_degmada_forms': DegmadaForm.objects.count(),
            'total_kafiilka_forms': KafiilkaForm.objects.count(),
        }
        
        return stats
    
    @staticmethod
    def get_documents_by_region():
        """Get documents grouped by region."""
        from .models import TravelDocument
        from django.db.models import Count
        
        return TravelDocument.objects.values('region').annotate(
            count=Count('id')
        ).order_by('-count')
    
    @staticmethod
    def get_recent_documents(days=30):
        """Get documents created in the last N days."""
        from .models import TravelDocument
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        return TravelDocument.objects.filter(created_at__gte=cutoff_date)


class NotificationHelper:
    """Helper functions for sending notifications."""
    
    @staticmethod
    def send_document_status_notification(document, new_status):
        """Send notification when document status changes."""
        # This could be extended to send emails, SMS, etc.
        notification_data = {
            'document_number': document.document_number,
            'full_name': document.full_name,
            'old_status': document.status,
            'new_status': new_status,
            'timestamp': datetime.now(),
        }
        # Placeholder for actual notification logic
        return notification_data
    
    @staticmethod
    def notify_pending_approval(documents):
        """Notify about documents pending approval."""
        pending = [doc for doc in documents if doc.status == 'filled']
        return pending


class ExportHelper:
    """Help export data to various formats."""
    
    @staticmethod
    def export_documents_to_dict(documents):
        """Convert document queryset to dictionary format."""
        result = []
        for doc in documents:
            data = {
                'document_number': doc.document_number,
                'full_name': doc.full_name,
                'date': doc.date.isoformat() if doc.date else None,
                'region': doc.region,
                'status': doc.get_status_display(),
                'created_at': doc.created_at.isoformat(),
            }
            result.append(data)
        return result
    
    @staticmethod
    def prepare_csv_data(documents):
        """Prepare data for CSV export."""
        headers = [
            'Document Number', 'Full Name', 'Date', 'Region', 
            'District', 'Status', 'Created At'
        ]
        rows = []
        
        for doc in documents:
            rows.append([
                doc.document_number,
                doc.full_name,
                doc.date.isoformat() if doc.date else '',
                doc.region,
                doc.district,
                doc.get_status_display(),
                doc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])
        
        return headers, rows

