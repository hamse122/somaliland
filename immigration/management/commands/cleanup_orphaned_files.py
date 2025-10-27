"""
Management command to cleanup orphaned media files.
"""
from django.core.management.base import BaseCommand
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Remove orphaned media files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write('Scanning for orphaned files...')
        
        from immigration.models import (
            TravelDocument, TravelDocumentChild,
            DegmadaFormMember, KafiilkaFormMember
        )
        
        # Get all photo file paths from database
        db_files = set()
        
        # Travel documents
        for doc in TravelDocument.objects.exclude(photo=''):
            if doc.photo:
                db_files.add(doc.photo.name)
        
        # Travel document children
        for child in TravelDocumentChild.objects.exclude(photo=''):
            if child.photo:
                db_files.add(child.photo.name)
        
        # Degmada form members
        for member in DegmadaFormMember.objects.exclude(photo=''):
            if member.photo:
                db_files.add(member.photo.name)
        
        # Kafiilka form members
        for member in KafiilkaFormMember.objects.exclude(photo=''):
            if member.photo:
                db_files.add(member.photo.name)
        
        self.stdout.write(f'Found {len(db_files)} files in database')
        
        # Scan media directory
        media_root = settings.MEDIA_ROOT
        orphaned_files = []
        
        for root, dirs, files in os.walk(media_root):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, media_root)
                if relative_path not in db_files:
                    orphaned_files.append(file_path)
        
        if orphaned_files:
            self.stdout.write(f'\nFound {len(orphaned_files)} orphaned files:')
            for file in orphaned_files[:10]:  # Show first 10
                self.stdout.write(f'  {file}')
            if len(orphaned_files) > 10:
                self.stdout.write(f'  ... and {len(orphaned_files) - 10} more')
            
            if not dry_run:
                confirmed = input('\nDelete these files? (yes/no): ')
                if confirmed.lower() == 'yes':
                    for file in orphaned_files:
                        try:
                            os.remove(file)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error deleting {file}: {e}'))
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'\nDeleted {len(orphaned_files)} orphaned files')
                    )
            else:
                self.stdout.write('\n(Dry run - no files were deleted)')
        else:
            self.stdout.write(self.style.SUCCESS('\nNo orphaned files found!'))

