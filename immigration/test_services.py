"""
Tests for immigration services.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import TravelDocument, DegmadaForm, KafiilkaForm
from .services import (
    TravelDocumentService, FormService, ValidationService
)
from .utils import DocumentValidator, DocumentNumberGenerator

User = get_user_model()


class TravelDocumentServiceTest(TestCase):
    """Tests for TravelDocumentService."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_travel_document(self):
        """Test creating a travel document."""
        form_data = {
            'full_name': 'Test User',
            'region': 'Hargeisa',
            'sponsor_name': 'Test Sponsor',
            'identification_number': 'TEST12345'
        }
        
        document = TravelDocumentService.create_travel_document(
            form_data,
            user=self.user
        )
        
        self.assertIsNotNone(document)
        self.assertEqual(document.full_name, 'Test User')
        self.assertIsNotNone(document.document_number)
        self.assertEqual(document.created_by, self.user)
    
    def test_create_travel_document_missing_required_fields(self):
        """Test creating document with missing required fields."""
        form_data = {
            'region': 'Hargeisa',
            # Missing full_name and sponsor_name
        }
        
        with self.assertRaises(ValidationError):
            TravelDocumentService.create_travel_document(form_data)
    
    def test_approve_document(self):
        """Test approving a document."""
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa',
            status='filled'
        )
        
        updated_document = TravelDocumentService.approve_document(document)
        
        self.assertEqual(updated_document.status, 'approved')
    
    def test_print_document(self):
        """Test printing a document."""
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa',
            status='approved'
        )
        
        updated_document = TravelDocumentService.print_document(document)
        
        self.assertEqual(updated_document.status, 'printed')
    
    def test_get_document_statistics(self):
        """Test getting document statistics."""
        TravelDocument.objects.create(
            full_name='User 1',
            region='Hargeisa',
            status='filled'
        )
        
        TravelDocument.objects.create(
            full_name='User 2',
            region='Hargeisa',
            status='approved'
        )
        
        stats = TravelDocumentService.get_document_statistics()
        
        self.assertEqual(stats['total'], 2)
        self.assertIn('by_status', stats)
        self.assertGreaterEqual(stats['recent_30_days'], 0)
    
    def test_search_documents(self):
        """Test searching documents."""
        document = TravelDocument.objects.create(
            full_name='John Doe',
            region='Hargeisa',
            document_number='TD-00123'
        )
        
        results = TravelDocumentService.search_documents('John')
        
        self.assertIn(document, results)


class FormServiceTest(TestCase):
    """Tests for FormService."""
    
    def test_create_degmada_form(self):
        """Test creating a degmada form."""
        form_data = {
            'company_name': 'Test Company',
            'sponsor_name': 'Test Sponsor',
            'gobolka': 'Woqooyi Galbeed',
            'degmada': 'Hargeisa'
        }
        
        form = FormService.create_degmada_form(form_data)
        
        self.assertIsNotNone(form)
        self.assertEqual(form.company_name, 'Test Company')
        self.assertIsNotNone(form.reference)
    
    def test_create_degmada_form_with_members(self):
        """Test creating degmada form with members."""
        form_data = {
            'company_name': 'Test Company',
            'sponsor_name': 'Test Sponsor'
        }
        
        members_data = [
            {
                'name': 'Member One',
                'nationality': 'Somali',
                'phone': '063123456',
                'id_number': 'ID12345'
            },
            {
                'name': 'Member Two',
                'nationality': 'Somali',
                'phone': '063123457',
                'id_number': 'ID12346'
            }
        ]
        
        form = FormService.create_degmada_form(form_data, members_data)
        
        self.assertEqual(form.members.count(), 2)
    
    def test_validate_form_completion(self):
        """Test form completion validation."""
        form = DegmadaForm.objects.create(
            company_name='Test Company'
            # Missing sponsor_name and pledge_name
        )
        
        errors = FormService.validate_form_completion(form)
        
        self.assertGreater(len(errors), 0)
        self.assertIn('sponsor_name is required', errors)


class ValidationServiceTest(TestCase):
    """Tests for ValidationService."""
    
    def test_validate_travel_document_valid(self):
        """Test validating a valid travel document."""
        data = {
            'full_name': 'Test User',
            'mother_name': 'Test Mother',
            'birth_date': '2000-01-01',
            'birth_place': 'Hargeisa',
            'identification_number': 'ID12345',
            'region': 'Hargeisa',
            'sponsor_name': 'Test Sponsor',
            'phone_number': '063123456'
        }
        
        errors = ValidationService.validate_travel_document(data)
        
        self.assertEqual(len(errors), 0)
    
    def test_validate_travel_document_missing_required(self):
        """Test validating document with missing required fields."""
        data = {
            'full_name': 'Test User'
            # Missing required fields
        }
        
        errors = ValidationService.validate_travel_document(data)
        
        self.assertGreater(len(errors), 0)
    
    def test_validate_sponsor_information(self):
        """Test validating sponsor information."""
        data = {
            'sponsor_name': 'Test Sponsor',
            'sponsor_id': 'SP12345',
            'sponsor_phone': '063123456'
        }
        
        errors = ValidationService.validate_sponsor_information(data)
        
        self.assertEqual(len(errors), 0)


class UtilityTests(TestCase):
    """Tests for utility functions."""
    
    def test_validate_phone_number(self):
        """Test phone number validation."""
        valid_numbers = ['063123456', '+25263123456', '0631234567']
        invalid_numbers = ['123', 'abc', '12345678901234']
        
        for number in valid_numbers:
            self.assertTrue(DocumentValidator.validate_phone_number(number))
        
        for number in invalid_numbers:
            self.assertFalse(DocumentValidator.validate_phone_number(number))
    
    def test_validate_id_number(self):
        """Test ID number validation."""
        valid_ids = ['ID12345', 'ABC123', '12345ABCDE']
        invalid_ids = ['id', '123', '!@#$%']
        
        for id_num in valid_ids:
            self.assertTrue(DocumentValidator.validate_id_number(id_num))
        
        for id_num in invalid_ids:
            self.assertFalse(DocumentValidator.validate_id_number(id_num))
    
    def test_calculate_age(self):
        """Test age calculation."""
        from datetime import date, timedelta
        
        birth_date = date.today() - timedelta(days=365*25)  # 25 years ago
        
        age = DocumentValidator.calculate_age(birth_date)
        
        self.assertEqual(age, 25)
    
    def test_generate_document_number(self):
        """Test document number generation."""
        number = DocumentNumberGenerator.generate_travel_document_number(100)
        
        self.assertEqual(number, 'TD-00101')

