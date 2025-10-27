"""
Signals for the immigration application.
"""
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import (
    TravelDocument, DegmadaForm, KafiilkaForm,
    TravelDocumentChild, DegmadaFormMember, KafiilkaFormMember
)


@receiver(pre_save, sender=TravelDocument)
def generate_document_number(sender, instance, **kwargs):
    """Generate document number if not provided."""
    if not instance.document_number:
        last_doc = TravelDocument.objects.order_by('-id').first()
        last_id = last_doc.id if last_doc else 0
        instance.document_number = f"TD-{str(last_id + 1).zfill(5)}"


@receiver(pre_save, sender=TravelDocument)
def update_modified_date(sender, instance, **kwargs):
    """Update the modified date when document is saved."""
    if instance.pk:
        # Document exists, this is an update
        # We can access the old data if needed
        pass
    # updated_at is auto-managed by auto_now


@receiver(post_save, sender=TravelDocument)
def notify_status_change(sender, instance, created, **kwargs):
    """Notify when document status changes."""
    if not created:
        # This is an update
        # Could send notifications, log changes, etc.
        # For now, just update the timestamp
        instance.updated_at = timezone.now()


@receiver(post_save, sender=TravelDocument)
def log_document_creation(sender, instance, created, **kwargs):
    """Log document creation."""
    if created:
        # Log the creation event
        # This could be sent to an audit log
        pass


@receiver(pre_save, sender=DegmadaForm)
def generate_degmada_reference(sender, instance, **kwargs):
    """Generate reference if not provided."""
    if not instance.reference:
        from .utils import DocumentNumberGenerator
        instance.reference = DocumentNumberGenerator.generate_degmada_reference()


@receiver(pre_save, sender=KafiilkaForm)
def generate_kafiilka_reference(sender, instance, **kwargs):
    """Generate reference if not provided."""
    if not instance.reference:
        from .utils import DocumentNumberGenerator
        instance.reference = DocumentNumberGenerator.generate_kafiilka_reference()


@receiver(post_save, sender=DegmadaFormMember)
def update_degmada_member_count(sender, instance, created, **kwargs):
    """Update member count and validate degmada form."""
    if created and instance.form:
        # Validate the form has minimum required members
        # Could add business logic here
        pass


@receiver(post_save, sender=KafiilkaFormMember)
def update_kafiilka_member_count(sender, instance, created, **kwargs):
    """Update member count and validate kafiilka form."""
    if created and instance.form:
        # Validate the form has minimum required members
        # Could add business logic here
        pass


@receiver(post_save, sender=TravelDocumentChild)
def update_child_photo(sender, instance, created, **kwargs):
    """Handle child photo updates."""
    if created and instance.photo:
        # Could add photo validation, resizing, etc.
        pass


@receiver(pre_delete, sender=TravelDocument)
def cleanup_travel_document(sender, instance, **kwargs):
    """Cleanup before deleting travel document."""
    # Clean up related files
    if instance.photo:
        instance.photo.delete(save=False)
    
    # Delete children photos
    for child in instance.children.all():
        if child.photo:
            child.photo.delete(save=False)


@receiver(pre_delete, sender=DegmadaForm)
def cleanup_degmada_form(sender, instance, **kwargs):
    """Cleanup before deleting degmada form."""
    # Delete member photos
    for member in instance.members.all():
        if member.photo:
            member.photo.delete(save=False)


@receiver(pre_delete, sender=KafiilkaForm)
def cleanup_kafiilka_form(sender, instance, **kwargs):
    """Cleanup before deleting kafiilka form."""
    # Delete member photos
    for member in instance.members.all():
        if member.photo:
            member.photo.delete(save=False)


@receiver(pre_delete, sender=DegmadaFormMember)
def cleanup_degmada_member(sender, instance, **kwargs):
    """Cleanup before deleting degmada form member."""
    # Delete photo
    if instance.photo:
        instance.photo.delete(save=False)


@receiver(pre_delete, sender=KafiilkaFormMember)
def cleanup_kafiilka_member(sender, instance, **kwargs):
    """Cleanup before deleting kafiilka form member."""
    # Delete photo
    if instance.photo:
        instance.photo.delete(save=False)


@receiver(post_save, sender=TravelDocument)
def validate_required_documents(sender, instance, **kwargs):
    """Validate required documents after save."""
    # Check if all required documents are present
    if instance.status == 'filled':
        # Could add validation logic here
        has_required = (
            instance.has_notayo or
            instance.has_sponsor_id or
            instance.has_company_license
        )
        
        if not has_required:
            # Log warning or set status to pending
            pass


@receiver(post_save, sender=TravelDocument)
def auto_approve_if_ready(sender, instance, **kwargs):
    """Auto-approve document if all conditions are met."""
    if instance.status == 'filled':
        # Check if all required documents are present
        has_required_docs = (
            instance.has_notayo or
            instance.has_sponsor_id or
            instance.has_company_license or
            instance.has_damaged_id
        )
        
        if has_required_docs and instance.officer_signature:
            # Could automatically approve if all conditions met
            # For now, just leave it as filled
            pass

