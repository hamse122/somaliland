"""
Custom validators for immigration application fields.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_phone_number(value):
    """Validator for phone numbers."""
    if not value:
        return
    
    # Allow Somaliland phone formats: +252 or 0 followed by digits
    pattern = r'^(\+252|0)[6-7][0-9]{7,8}$'
    
    if not re.match(pattern, value.replace(' ', '').replace('-', '')):
        raise ValidationError(
            _('Invalid phone number format. Use format: +2526XXXXXXXX or 06XXXXXXXX'),
            params={'value': value},
        )


def validate_id_number(value):
    """Validator for identification numbers."""
    if not value:
        return
    
    # Should be alphanumeric, 5-20 characters
    if not re.match(r'^[A-Z0-9]{5,20}$', value.upper()):
        raise ValidationError(
            _('Invalid ID number format. Must be alphanumeric, 5-20 characters.'),
            params={'value': value},
        )


def validate_birth_date(value):
    """Validator for birth dates."""
    from datetime import date
    
    if value and value > date.today():
        raise ValidationError(
            _('Birth date cannot be in the future.'),
            params={'value': value},
        )
    
    # Check if date is not too far in the past (reasonable age)
    if value:
        from .utils import DocumentValidator
        age = DocumentValidator.calculate_age(value)
        if age and age > 120:
            raise ValidationError(
                _('Invalid birth date. Age seems unrealistic.'),
                params={'value': value},
            )


def validate_date_not_future(value):
    """Validator to ensure date is not in the future."""
    from datetime import date
    
    if value and value > date.today():
        raise ValidationError(
            _('Date cannot be in the future.'),
            params={'value': value},
        )


def validate_name_format(value):
    """Validator for name fields."""
    if not value:
        return
    
    # Check for only letters, spaces, apostrophes, and dashes
    if not re.match(r"^[A-Za-z\s'-]+$", value):
        raise ValidationError(
            _('Name can only contain letters, spaces, hyphens, and apostrophes.'),
            params={'value': value},
        )
    
    # Check minimum length
    if len(value.strip()) < 2:
        raise ValidationError(
            _('Name must be at least 2 characters long.'),
            params={'value': value},
        )


def validate_document_number_format(value):
    """Validator for document numbers."""
    if not value:
        return
    
    # Should match pattern like: TD-00001
    if not re.match(r'^TD-\d{5}$', value):
        raise ValidationError(
            _('Invalid document number format. Should be like TD-00001.'),
            params={'value': value},
        )


def validate_license_number(value):
    """Validator for license numbers."""
    if not value:
        return
    
    # Basic validation - alphanumeric, 4-20 characters
    if not re.match(r'^[A-Z0-9]{4,20}$', value.upper()):
        raise ValidationError(
            _('Invalid license number format.'),
            params={'value': value},
        )


def validate_email_optional(value):
    """Validator for optional email addresses."""
    if not value:
        return
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Invalid email address format.'),
            params={'value': value},
        )


def validate_sponsor_type(value):
    """Validator for sponsor type choices."""
    valid_types = ['SHASI', 'WADAR']
    if value and value not in valid_types:
        raise ValidationError(
            _('Invalid sponsor type. Must be SHASI or WADAR.'),
            params={'value': value},
        )


def validate_region(value):
    """Validator for region field."""
    if not value:
        return
    
    # Common Somaliland regions
    valid_regions = [
        'Hargeisa', 'Burao', 'Berbera', 'Borama',
        'Awdal', 'Sanaag', 'Sool', 'Togdheer',
        'Woqooyi Galbeed', 'Sahil'
    ]
    
    # Allow flexibility - just check minimum length and format
    if len(value.strip()) < 2:
        raise ValidationError(
            _('Region name must be at least 2 characters.'),
            params={'value': value},
        )


def validate_district(value):
    """Validator for district field."""
    if not value:
        return
    
    if len(value.strip()) < 2:
        raise ValidationError(
            _('District name must be at least 2 characters.'),
            params={'value': value},
        )


def validate_age_for_adults(value):
    """Validator to ensure age is 18+ for certain applications."""
    from .utils import DocumentValidator
    
    if value:
        age = DocumentValidator.calculate_age(value)
        if age and age < 18:
            raise ValidationError(
                _('Applicant must be at least 18 years old.'),
                params={'value': value},
            )


def validate_reference_format(value):
    """Validator for form reference numbers."""
    if not value:
        return
    
    # Check if it matches expected format (DEG-YYYYMMDD-HHMMSS or KAF-YYYYMMDD-HHMMSS)
    if not re.match(r'^(DEG|KAF)-\d{8}-\d{6}$', value):
        raise ValidationError(
            _('Invalid reference format. Should be like DEG-20250101-120000.'),
            params={'value': value},
        )


def validate_positive_integer(value):
    """Validator to ensure positive integers."""
    if value is not None and value < 0:
        raise ValidationError(
            _('Value must be a positive number.'),
            params={'value': value},
        )


def validate_text_field_length(value, max_length=None, min_length=None):
    """Generic validator for text field lengths."""
    if not value:
        return
    
    if min_length and len(value) < min_length:
        raise ValidationError(
            _('Text must be at least %(min)d characters long.'),
            params={'min': min_length, 'value': value},
        )
    
    if max_length and len(value) > max_length:
        raise ValidationError(
            _('Text must not exceed %(max)d characters.'),
            params={'max': max_length, 'value': value},
        )


def validate_image_dimensions(value, max_width=None, max_height=None):
    """Validator for image dimensions (to be used in forms)."""
    from PIL import Image
    from django.core.files.uploadedfile import UploadedFile
    
    if not value or not isinstance(value, UploadedFile):
        return
    
    try:
        with Image.open(value) as img:
            width, height = img.size
            
            if max_width and width > max_width:
                raise ValidationError(
                    _('Image width must not exceed %(width)d pixels.'),
                    params={'width': max_width},
                )
            
            if max_height and height > max_height:
                raise ValidationError(
                    _('Image height must not exceed %(height)d pixels.'),
                    params={'height': max_height},
                )
    except Exception as e:
        raise ValidationError(
            _('Invalid image file.'),
            params={'value': value},
        )


def validate_file_size(value, max_size_mb=5):
    """Validator for file size."""
    if not value:
        return
    
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if hasattr(value, 'size') and value.size > max_size_bytes:
        raise ValidationError(
            _('File size must not exceed %(size)d MB.'),
            params={'size': max_size_mb, 'value': value},
        )

