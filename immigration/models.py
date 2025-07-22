from django.db import models

class DegmadaForm(models.Model):
    reference = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True, null=True)
    gobolka = models.CharField(max_length=100, blank=True)
    degmada = models.CharField(max_length=100, blank=True)
    
    # Section A: Company/Organization
    company_name = models.CharField(max_length=200, blank=True)
    company_license = models.CharField(max_length=100, blank=True)
    establishment_period = models.CharField(max_length=100, blank=True)
    working_employees = models.IntegerField(blank=True, null=True)
    company_region = models.CharField(max_length=100, blank=True)
    company_district = models.CharField(max_length=100, blank=True)
    
    # Section B: Sponsor (Individual)
    sponsor_name = models.CharField(max_length=200, blank=True)
    sponsor_id = models.CharField(max_length=50, blank=True)
    sponsor_phone = models.CharField(max_length=20, blank=True)
    sponsor_contact = models.CharField(max_length=20, blank=True)
    sponsor_address = models.TextField(blank=True)
    
    # Section C: Approved People
    pledge_name = models.CharField(max_length=200, blank=True)
    pledge_signature = models.CharField(max_length=200, blank=True)
    district_leader_name = models.CharField(max_length=200, blank=True)
    district_leader_signature = models.CharField(max_length=200, blank=True)
    filled_date = models.DateField(blank=True, null=True)
    attachment_types = models.CharField(max_length=200, blank=True)
    special_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.reference}"

class DegmadaFormMember(models.Model):
    form = models.ForeignKey(DegmadaForm, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='degmada_photos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class KafiilkaForm(models.Model):
    reference = models.CharField(max_length=100, blank=True)
    date = models.DateField(blank=True, null=True)
    gobolka = models.CharField(max_length=100, blank=True)
    degmada = models.CharField(max_length=100, blank=True)
    
    # Section A: Company/Organization
    company_name = models.CharField(max_length=200, blank=True)
    company_license = models.CharField(max_length=100, blank=True)
    establishment_period = models.CharField(max_length=100, blank=True)
    working_employees = models.IntegerField(blank=True, null=True)
    company_region = models.CharField(max_length=100, blank=True)
    company_district = models.CharField(max_length=100, blank=True)
    
    # Section B: Sponsor
    sponsor_type = models.CharField(max_length=10, choices=[('SHASI', 'Individual'), ('WADAR', 'Group')], blank=True)
    sponsor_name = models.CharField(max_length=200, blank=True)
    sponsor_id = models.CharField(max_length=50, blank=True)
    sponsor_phone = models.CharField(max_length=20, blank=True)
    sponsor_contact = models.CharField(max_length=20, blank=True)
    sponsor_address = models.TextField(blank=True)
    
    # Section C: Approved People
    pledge_name = models.CharField(max_length=200, blank=True)
    pledge_signature = models.CharField(max_length=200, blank=True)
    district_leader_name = models.CharField(max_length=200, blank=True)
    district_leader_signature = models.CharField(max_length=200, blank=True)
    filled_date = models.DateField(blank=True, null=True)
    attachment_types = models.CharField(max_length=200, blank=True)
    special_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.reference}"

class KafiilkaFormMember(models.Model):
    form = models.ForeignKey(KafiilkaForm, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='kafiilka_photos/', blank=True, null=True)
    
    def __str__(self):
        return self.name

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TravelDocument(models.Model):
    STATUS_CHOICES = [
        ('filled', 'Waa la Buxiyay'),
        ('approved', 'Waa la Ogolaaday'),
        ('printed', 'Waa la Daabacay'),
    ]
    
    # Document Information
    region_office = models.CharField(max_length=100, blank=True, verbose_name="Xafiiska Gobolka")
    date = models.DateField(blank=True, null=True, verbose_name="Taariikhda")
    document_number = models.CharField(max_length=50, blank=True, unique=True, verbose_name="Lambarka Warqadda")
    
    # Personal Information
    full_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca oo Afaran")
    mother_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Hooyada")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda Dhalasho")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="Goobta Dhalasho")
    identification_number = models.CharField(max_length=50, blank=True, verbose_name="Aqoonsi Lambar")
    region = models.CharField(max_length=100, blank=True, verbose_name="Gobolka")
    workplace = models.CharField(max_length=100, blank=True, verbose_name="Goobta Shaqo")
    sponsor_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Wakiilka")
    
    # Contact Information
    citizen_card = models.CharField(max_length=50, blank=True, verbose_name="Card-ka Muwadinka")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telephone Lambar")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Jinsiyadda")
    district = models.CharField(max_length=100, blank=True, verbose_name="Degmada")
    job_type = models.CharField(max_length=100, blank=True, verbose_name="Nooca Shaqo")
    license_number = models.CharField(max_length=50, blank=True, verbose_name="Liisan Lambar")
    contact_number = models.CharField(max_length=20, blank=True, verbose_name="Contact Number")
    
    # Immigration Officer Section
    filled_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda la buuxiyay")
    has_notayo = models.BooleanField(default=False, verbose_name="Notaayo")
    has_sponsor_id = models.BooleanField(default=False, verbose_name="ID-ga Kafiilka")
    has_damaged_id = models.BooleanField(default=False, verbose_name="Aqoonsiga Ladamiintaha")
    has_company_license = models.BooleanField(default=False, verbose_name="Liisanka Shirkada")
    has_other_documents = models.BooleanField(default=False, verbose_name="Hadii wax kale jiro")
    immigration_officer_notes = models.TextField(blank=True, verbose_name="Faahfaahin Gaar ah")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=True, verbose_name="Marxalada uu Marayo")
    card_number = models.CharField(max_length=50, blank=True, verbose_name="Card Number")
    officer_signature = models.CharField(max_length=200, blank=True, verbose_name="Signature")
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_documents')
    
    photo = models.ImageField(upload_to='travel_documents/photos/', blank=True, null=True, verbose_name="Sawirka")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Travel Document"
        verbose_name_plural = "Travel Documents"
    
    def __str__(self):
        return f"{self.full_name} - {self.document_number}"
    
    def get_absolute_url(self):
        return reverse('travel_document_detail', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        if not self.document_number:
            # Generate document number if not provided
            last_doc = TravelDocument.objects.order_by('-id').first()
            last_id = last_doc.id if last_doc else 0
            self.document_number = f"TD-{str(last_id + 1).zfill(5)}"
        super().save(*args, **kwargs)

class TravelDocumentChild(models.Model):
    document = models.ForeignKey(TravelDocument, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=200, verbose_name="Magaca")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda Dhalasho")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="Goobta Dhalasho")
    photo = models.ImageField(upload_to='travel_documents/children/', blank=True, null=True, verbose_name="Sawirka")
    
    class Meta:
        verbose_name = "Travel Document Child"
        verbose_name_plural = "Travel Document Children"
    
    def __str__(self):
        return self.name