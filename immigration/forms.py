"""
Enhanced Django forms for the immigration application.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import (
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember,
    TravelDocument, TravelDocumentChild
)
from .validators import validate_phone_number, validate_id_number, validate_birth_date


class DegmadaFormForm(forms.ModelForm):
    """Form for creating and editing Degmada forms."""
    
    class Meta:
        model = DegmadaForm
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'filled_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'sponsor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sponsor name'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'
                elif isinstance(field.widget, forms.FileInput):
                    field.widget.attrs['class'] = 'form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'


class DegmadaFormMemberForm(forms.ModelForm):
    """Form for creating Degmada form members."""
    
    class Meta:
        model = DegmadaFormMember
        fields = ['name', 'nationality', 'birth_date', 'phone', 'id_number', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter member name'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter nationality'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+252 or 0XXXXXXXXX'
            }),
            'id_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ID number'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone')
        if phone and not validate_phone_number(phone):
            raise ValidationError(_('Invalid phone number format.'))
        return phone
    
    def clean_id_number(self):
        """Validate ID number format."""
        id_number = self.cleaned_data.get('id_number')
        if id_number and not validate_id_number(id_number):
            raise ValidationError(_('Invalid ID number format.'))
        return id_number
    
    def clean_birth_date(self):
        """Validate birth date."""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            validate_birth_date(birth_date)
        return birth_date


DegmadaFormMemberFormSet = forms.inlineformset_factory(
    DegmadaForm,
    DegmadaFormMember,
    form=DegmadaFormMemberForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class KafiilkaFormForm(forms.ModelForm):
    """Form for creating and editing Kafiilka forms."""
    
    class Meta:
        model = KafiilkaForm
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'filled_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'sponsor_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


class KafiilkaFormMemberForm(forms.ModelForm):
    """Form for creating Kafiilka form members."""
    
    class Meta:
        model = KafiilkaFormMember
        fields = ['name', 'nationality', 'birth_date', 'phone', 'id_number', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+252 or 0XXXXXXXXX'
            }),
            'id_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
    
    def clean_phone(self):
        """Validate phone number."""
        phone = self.cleaned_data.get('phone')
        if phone and not validate_phone_number(phone):
            raise ValidationError(_('Invalid phone number format.'))
        return phone
    
    def clean_id_number(self):
        """Validate ID number."""
        id_number = self.cleaned_data.get('id_number')
        if id_number and not validate_id_number(id_number):
            raise ValidationError(_('Invalid ID number format.'))
        return id_number
    
    def clean_birth_date(self):
        """Validate birth date."""
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            validate_birth_date(birth_date)
        return birth_date


KafiilkaFormMemberFormSet = forms.inlineformset_factory(
    KafiilkaForm,
    KafiilkaFormMember,
    form=KafiilkaFormMemberForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class TravelDocumentForm(forms.ModelForm):
    """Form for creating and editing travel documents."""
    
    class Meta:
        model = TravelDocument
        exclude = ['created_at', 'updated_at', 'created_by', 'document_number']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'filled_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'immigration_officer_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter any special notes or remarks'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+252 or 0XXXXXXXXX'
            }),
            'region': forms.Select(attrs={
                'class': 'form-control'
            }),
            'district': forms.Select(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['has_notayo', 'has_sponsor_id', 'has_damaged_id', 
                                'has_company_license', 'has_other_documents']:
                if 'class' not in field.widget.attrs:
                    if isinstance(field.widget, forms.CheckboxInput):
                        field.widget.attrs['class'] = 'form-check-input'
                    else:
                        field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'
    
    def clean_phone_number(self):
        """Validate phone number format."""
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not validate_phone_number(phone_number):
            raise ValidationError(_('Invalid phone number format. Use +252 or 0XXXXXXXXX'))
        return phone_number
    
    def clean_identification_number(self):
        """Validate identification number."""
        id_number = self.cleaned_data.get('identification_number')
        if id_number and not validate_id_number(id_number):
            raise ValidationError(_('Invalid identification number format.'))
        return id_number


class TravelDocumentChildForm(forms.ModelForm):
    """Form for creating and editing travel document children."""
    
    class Meta:
        model = TravelDocumentChild
        fields = ['name', 'birth_date', 'birth_place', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter child name'
            }),
            'birth_place': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'


TravelDocumentChildFormSet = forms.inlineformset_factory(
    TravelDocument,
    TravelDocumentChild,
    form=TravelDocumentChildForm,
    extra=1,
    can_delete=True
)
