from django import forms
from .models import (
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember,
    TravelDocument, TravelDocumentChild
)

class DegmadaFormForm(forms.ModelForm):
    class Meta:
        model = DegmadaForm
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'filled_date': forms.DateInput(attrs={'type': 'date'}),
        }

class DegmadaFormMemberForm(forms.ModelForm):
    class Meta:
        model = DegmadaFormMember
        fields = ['name', 'nationality', 'birth_date', 'phone', 'id_number', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

DegmadaFormMemberFormSet = forms.inlineformset_factory(
    DegmadaForm, DegmadaFormMember, 
    form=DegmadaFormMemberForm,
    extra=1,
    can_delete=True
)

class KafiilkaFormForm(forms.ModelForm):
    class Meta:
        model = KafiilkaForm
        exclude = ['created_at', 'updated_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'filled_date': forms.DateInput(attrs={'type': 'date'}),
        }

class KafiilkaFormMemberForm(forms.ModelForm):
    class Meta:
        model = KafiilkaFormMember
        fields = ['name', 'nationality', 'birth_date', 'phone', 'id_number', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

KafiilkaFormMemberFormSet = forms.inlineformset_factory(
    KafiilkaForm, KafiilkaFormMember, 
    form=KafiilkaFormMemberForm,
    extra=1,
    can_delete=True
)

from django import forms
from .models import TravelDocument, TravelDocumentChild

class TravelDocumentForm(forms.ModelForm):
    class Meta:
        model = TravelDocument
        exclude = ['created_at', 'updated_at', 'created_by', 'document_number']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'filled_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'immigration_officer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['has_notayo', 'has_sponsor_id', 'has_damaged_id', 
                                'has_company_license', 'has_other_documents']:
                field.widget.attrs['class'] = 'form-control'
            if field_name in ['has_notayo', 'has_sponsor_id', 'has_damaged_id',
                            'has_company_license', 'has_other_documents']:
                field.widget.attrs['class'] = 'form-check-input'

class TravelDocumentChildForm(forms.ModelForm):
    class Meta:
        model = TravelDocumentChild
        fields = ['name', 'birth_date', 'birth_place', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

TravelDocumentChildFormSet = forms.inlineformset_factory(
    TravelDocument, TravelDocumentChild, 
    form=TravelDocumentChildForm,
    extra=1,
    can_delete=True
)