from django.db import models

class DegmadaForm(models.Model):
    """Model for Degmada (District) immigration forms."""
    reference = models.CharField(max_length=100, blank=True, unique=True)
    date = models.DateField(blank=True, null=True)
    gobolka = models.CharField(max_length=100, blank=True, verbose_name="Gobolka")
    degmada = models.CharField(max_length=100, blank=True, verbose_name="Degmada")
    
    # Section A: Company/Organization
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Shirkada")
    company_license = models.CharField(max_length=100, blank=True, verbose_name="Liisan Lambar")
    establishment_period = models.CharField(max_length=100, blank=True, verbose_name="Wakhtiga la Aasaasay")
    working_employees = models.IntegerField(blank=True, null=True, verbose_name="Shaqaalaha Shaqeeya")
    company_region = models.CharField(max_length=100, blank=True, verbose_name="Gobolka Shirkada")
    company_district = models.CharField(max_length=100, blank=True, verbose_name="Degmada Shirkada")
    
    # Section B: Sponsor (Individual)
    sponsor_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Kafiilka")
    sponsor_id = models.CharField(max_length=50, blank=True, verbose_name="Aqoonsi Lambar")
    sponsor_phone = models.CharField(max_length=20, blank=True, verbose_name="Telephone")
    sponsor_contact = models.CharField(max_length=20, blank=True, verbose_name="Contact")
    sponsor_address = models.TextField(blank=True, verbose_name="Ciwaanka")
    
    # Section C: Approved People
    pledge_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Damaashaadaha")
    pledge_signature = models.CharField(max_length=200, blank=True, verbose_name="Saaxiibeynta")
    district_leader_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Madaxa Degmada")
    district_leader_signature = models.CharField(max_length=200, blank=True, verbose_name="Saaxiibeynta")
    filled_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda la Buxiyay")
    attachment_types = models.CharField(max_length=200, blank=True, verbose_name="Nooca Lifaaqyada")
    special_notes = models.TextField(blank=True, verbose_name="Faahfaahin Gaar ah")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Taariikhda la Sameeyay")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Taariikhda la Cusbooneysiiyay")
    
    class Meta:
        verbose_name = "Foomka Degmada"
        verbose_name_plural = "Foomyada Degmada"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['date']),
            models.Index(fields=['company_name']),
        ]
    
    def __str__(self):
        return f"{self.company_name} - {self.reference}"
    
    def get_member_count(self):
        """Return the number of members in this form."""
        return self.members.count()
    
    def is_complete(self):
        """Check if all required fields are filled."""
        required_fields = [
            'company_name', 'sponsor_name', 'pledge_name',
            'district_leader_name'
        ]
        return all(getattr(self, field) for field in required_fields)

class DegmadaFormMember(models.Model):
    """Model for members in Degmada forms."""
    form = models.ForeignKey(DegmadaForm, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200, verbose_name="Magaca")
    nationality = models.CharField(max_length=100, verbose_name="Jinsiyadda")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda Dhalasho")
    phone = models.CharField(max_length=20, verbose_name="Telephone")
    id_number = models.CharField(max_length=50, verbose_name="Aqoonsi Lambar")
    photo = models.ImageField(upload_to='degmada_photos/', blank=True, null=True, verbose_name="Sawirka")
    
    class Meta:
        verbose_name = "Xubinta Foomka Degmada"
        verbose_name_plural = "Xubnaha Foomyada Degmada"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_age(self):
        """Calculate age from birth date."""
        from django.utils import timezone
        from datetime import date
        
        if not self.birth_date:
            return None
        
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

class KafiilkaForm(models.Model):
    """Model for Kafiilka (Sponsor) immigration forms."""
    
    SPONSOR_TYPE_CHOICES = [
        ('SHASI', 'Individual'),
        ('WADAR', 'Group'),
    ]
    
    reference = models.CharField(max_length=100, blank=True, unique=True)
    date = models.DateField(blank=True, null=True, verbose_name="Taariikhda")
    gobolka = models.CharField(max_length=100, blank=True, verbose_name="Gobolka")
    degmada = models.CharField(max_length=100, blank=True, verbose_name="Degmada")
    
    # Section A: Company/Organization
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Shirkada")
    company_license = models.CharField(max_length=100, blank=True, verbose_name="Liisan Lambar")
    establishment_period = models.CharField(max_length=100, blank=True, verbose_name="Wakhtiga la Aasaasay")
    working_employees = models.IntegerField(blank=True, null=True, verbose_name="Shaqaalaha Shaqeeya")
    company_region = models.CharField(max_length=100, blank=True, verbose_name="Gobolka Shirkada")
    company_district = models.CharField(max_length=100, blank=True, verbose_name="Degmada Shirkada")
    
    # Section B: Sponsor
    sponsor_type = models.CharField(
        max_length=10,
        choices=SPONSOR_TYPE_CHOICES,
        blank=True,
        verbose_name="Nooca Kafiilka"
    )
    sponsor_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Kafiilka")
    sponsor_id = models.CharField(max_length=50, blank=True, verbose_name="Aqoonsi Lambar")
    sponsor_phone = models.CharField(max_length=20, blank=True, verbose_name="Telephone")
    sponsor_contact = models.CharField(max_length=20, blank=True, verbose_name="Contact")
    sponsor_address = models.TextField(blank=True, verbose_name="Ciwaanka")
    
    # Section C: Approved People
    pledge_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Damaashaadaha")
    pledge_signature = models.CharField(max_length=200, blank=True, verbose_name="Saaxiibeynta")
    district_leader_name = models.CharField(max_length=200, blank=True, verbose_name="Magaca Madaxa Degmada")
    district_leader_signature = models.CharField(max_length=200, blank=True, verbose_name="Saaxiibeynta")
    filled_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda la Buxiyay")
    attachment_types = models.CharField(max_length=200, blank=True, verbose_name="Nooca Lifaaqyada")
    special_notes = models.TextField(blank=True, verbose_name="Faahfaahin Gaar ah")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Taariikhda la Sameeyay")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Taariikhda la Cusbooneysiiyay")
    
    class Meta:
        verbose_name = "Foomka Kafiilka"
        verbose_name_plural = "Foomyada Kafiilka"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['sponsor_type']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.company_name} - {self.reference}"
    
    def get_member_count(self):
        """Return the number of members in this form."""
        return self.members.count()
    
    def is_individual_sponsor(self):
        """Check if this is an individual sponsor form."""
        return self.sponsor_type == 'SHASI'
    
    def is_group_sponsor(self):
        """Check if this is a group sponsor form."""
        return self.sponsor_type == 'WADAR'

class KafiilkaFormMember(models.Model):
    """Model for members in Kafiilka forms."""
    form = models.ForeignKey(KafiilkaForm, on_delete=models.CASCADE, related_name='members')
    name = models.CharField(max_length=200, verbose_name="Magaca")
    nationality = models.CharField(max_length=100, verbose_name="Jinsiyadda")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda Dhalasho")
    phone = models.CharField(max_length=20, verbose_name="Telephone")
    id_number = models.CharField(max_length=50, verbose_name="Aqoonsi Lambar")
    photo = models.ImageField(upload_to='kafiilka_photos/', blank=True, null=True, verbose_name="Sawirka")
    
    class Meta:
        verbose_name = "Xubinta Foomka Kafiilka"
        verbose_name_plural = "Xubnaha Foomyada Kafiilka"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_age(self):
        """Calculate age from birth date."""
        from django.utils import timezone
        from datetime import date
        
        if not self.birth_date:
            return None
        
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

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
        verbose_name = "Warqadda Safari"
        verbose_name_plural = "Warqadaha Safari"
        indexes = [
            models.Index(fields=['document_number']),
            models.Index(fields=['status']),
            models.Index(fields=['region']),
            models.Index(fields=['created_at']),
        ]
    
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
    
    def get_status_color(self):
        """Return color code for status badge."""
        colors = {
            'filled': '#FFA500',     # Orange
            'approved': '#00FF00',    # Green
            'printed': '#0000FF',     # Blue
        }
        return colors.get(self.status, '#000000')
    
    def get_children_count(self):
        """Return the number of children."""
        return self.children.count()
    
    def can_be_approved(self):
        """Check if document can be approved."""
        return self.status == 'filled' and any([
            self.has_notayo,
            self.has_sponsor_id,
            self.has_company_license,
            self.has_damaged_id
        ])
    
    def can_be_printed(self):
        """Check if document can be printed."""
        return self.status == 'approved'

class TravelDocumentChild(models.Model):
    document = models.ForeignKey(TravelDocument, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=200, verbose_name="Magaca")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Taariikhda Dhalasho")
    birth_place = models.CharField(max_length=100, blank=True, verbose_name="Goobta Dhalasho")
    photo = models.ImageField(upload_to='travel_documents/children/', blank=True, null=True, verbose_name="Sawirka")
    
    class Meta:
        verbose_name = "Cunuga Warqadda Safari"
        verbose_name_plural = "Carruurta Warqadaha Safari"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_age(self):
        """Calculate age from birth date."""
        from datetime import date
        
        if not self.birth_date:
            return None
        
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )