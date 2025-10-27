from django.contrib import admin
from .models import (
    TravelDocument, TravelDocumentChild,
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember
)

# Import enhanced admin
from .enhanced_admin import *

# Models are already registered in enhanced_admin.py
