"""
Tests for immigration models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import (
    TravelDocument, TravelDocumentChild,
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember
)
from django.core.exceptions import ValidationError

User = get_user_model()


class TravelDocumentModelTest(TestCase):
    """Tests for TravelDocument model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_travel_document(self):
        """Test creating a travel document."""
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa',
            sponsor_name='Test Sponsor',
            identification_number='TEST12345'
        )
        
        self.assertEqual(document.full_name, 'Test User')
        self.assertEqual(document.region, 'Hargeisa')
        self.assertIsNotNone(document.document_number)
        self.assertTrue(document.document_number.startswith('TD-'))
    
    def test_document_number_generation(self):
        """Test automatic document number generation."""
        doc1 = TravelDocument.objects.create(
            full_name='User 1',
            region='Hargeisa'
        )
        
        doc2 = TravelDocument.objects.create(
            full_name='User 2',
            region='Hargeisa'
        )
        
        self.assertNotEqual(doc1.document_number, doc2.document_number)
        self.assertTrue(doc1.document_number.endswith('00001'))
        self.assertTrue(doc2.document_number.endswith('00002'))
    
    def test_document_status_choices(self):
        """Test document status choices."""
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa'
        )
        
        # Test valid statuses
        for status_code, status_display in TravelDocument.STATUS_CHOICES:
            document.status = status_code
            document.save()
            self.assertEqual(document.status, status_code)
            self.assertIn(status_display, [choice[1] for choice in TravelDocument.STATUS_CHOICES])
    
    def test_document_str_representation(self):
        """Test string representation of documents."""
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa',
            document_number='TD-TEST'
        )
        
        self.assertEqual(str(document), 'Test User - TD-TEST')
    
    def test_document_with_children(self):
        """Test document with children."""
        document = TravelDocument.objects.create(
            full_name='Parent User',
            region='Hargeisa'
        )
        
        child1 = TravelDocumentChild.objects.create(
            document=document,
            name='Child One',
            birth_place='Hargeisa'
        )
        
        child2 = TravelDocumentChild.objects.create(
            document=document,
            name='Child Two',
            birth_place='Hargeisa'
        )
        
        self.assertEqual(document.children.count(), 2)
        self.assertIn(child1, document.children.all())
        self.assertIn(child2, document.children.all())


class DegmadaFormModelTest(TestCase):
    """Tests for DegmadaForm model."""
    
    def test_create_degmada_form(self):
        """Test creating a degmada form."""
        form = DegmadaForm.objects.create(
            company_name='Test Company',
            sponsor_name='Test Sponsor',
            gobolka='Woqooyi Galbeed',
            degmada='Hargeisa'
        )
        
        self.assertEqual(form.company_name, 'Test Company')
        self.assertIsNotNone(form.reference)
    
    def test_degmada_form_with_members(self):
        """Test degmada form with members."""
        form = DegmadaForm.objects.create(
            company_name='Test Company',
            sponsor_name='Test Sponsor'
        )
        
        member1 = DegmadaFormMember.objects.create(
            form=form,
            name='Member One',
            nationality='Somali',
            phone='063123456',
            id_number='ID12345'
        )
        
        member2 = DegmadaFormMember.objects.create(
            form=form,
            name='Member Two',
            nationality='Somali',
            phone='063123457',
            id_number='ID12346'
        )
        
        self.assertEqual(form.members.count(), 2)
        self.assertIn(member1, form.members.all())
        self.assertIn(member2, form.members.all())


class KafiilkaFormModelTest(TestCase):
    """Tests for KafiilkaForm model."""
    
    def test_create_kafiilka_form(self):
        """Test creating a kafiilka form."""
        form = KafiilkaForm.objects.create(
            company_name='Test Company',
            sponsor_name='Test Sponsor',
            sponsor_type='SHASI',
            gobolka='Woqooyi Galbeed'
        )
        
        self.assertEqual(form.company_name, 'Test Company')
        self.assertEqual(form.sponsor_type, 'SHASI')
        self.assertIsNotNone(form.reference)
    
    def test_kafiilka_form_sponsor_types(self):
        """Test kafiilka form sponsor types."""
        form_individual = KafiilkaForm.objects.create(
            company_name='Test Company',
            sponsor_type='SHASI'
        )
        
        form_group = KafiilkaForm.objects.create(
            company_name='Test Company 2',
            sponsor_type='WADAR'
        )
        
        self.assertEqual(form_individual.sponsor_type, 'SHASI')
        self.assertEqual(form_group.sponsor_type, 'WADAR')
        self.assertEqual(form_individual.get_sponsor_type_display(), 'Individual')
        self.assertEqual(form_group.get_sponsor_type_display(), 'Group')


class ModelRelationsTest(TestCase):
    """Tests for model relationships."""
    
    def test_travel_document_created_by_user(self):
        """Test travel document user relationship."""
        user = User.objects.create_user(
            username='creator',
            password='test123'
        )
        
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa',
            created_by=user
        )
        
        self.assertEqual(document.created_by, user)
        self.assertEqual(user.created_documents.first(), document)
    
    def test_degmada_form_members_cascade_delete(self):
        """Test cascade delete for form members."""
        form = DegmadaForm.objects.create(
            company_name='Test Company'
        )
        
        member = DegmadaFormMember.objects.create(
            form=form,
            name='Test Member',
            nationality='Somali',
            phone='063123456',
            id_number='ID123'
        )
        
        member_id = member.id
        
        # Delete form
        form.delete()
        
        # Member should be deleted
        self.assertFalse(DegmadaFormMember.objects.filter(id=member_id).exists())
    
    def test_travel_document_children_cascade_delete(self):
        """Test cascade delete for document children."""
        document = TravelDocument.objects.create(
            full_name='Test User',
            region='Hargeisa'
        )
        
        child = TravelDocumentChild.objects.create(
            document=document,
            name='Test Child',
            birth_place='Hargeisa'
        )
        
        child_id = child.id
        
        # Delete document
        document.delete()
        
        # Child should be deleted
        self.assertFalse(TravelDocumentChild.objects.filter(id=child_id).exists())

