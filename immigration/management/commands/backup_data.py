"""
Management command to backup immigration data.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
import json
import os


class Command(BaseCommand):
    help = 'Backup immigration data to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='backup.json',
            help='Output filename (default: backup.json)'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        
        self.stdout.write('Starting data backup...')
        
        # Import models
        from immigration.models import (
            TravelDocument, DegmadaForm, KafiilkaForm,
            TravelDocumentChild, DegmadaFormMember, KafiilkaFormMember
        )
        
        backup_data = {
            'timestamp': timezone.now().isoformat(),
            'travel_documents': [],
            'degmada_forms': [],
            'kafiilka_forms': [],
        }
        
        # Backup Travel Documents
        self.stdout.write('Backing up Travel Documents...')
        for doc in TravelDocument.objects.all():
            data = {
                'document_number': doc.document_number,
                'region_office': doc.region_office,
                'date': doc.date.isoformat() if doc.date else None,
                'full_name': doc.full_name,
                'mother_name': doc.mother_name,
                'birth_date': doc.birth_date.isoformat() if doc.birth_date else None,
                'birth_place': doc.birth_place,
                'identification_number': doc.identification_number,
                'region': doc.region,
                'district': doc.district,
                'workplace': doc.workplace,
                'sponsor_name': doc.sponsor_name,
                'phone_number': doc.phone_number,
                'status': doc.status,
                'created_at': doc.created_at.isoformat() if doc.created_at else None,
            }
            backup_data['travel_documents'].append(data)
        
        # Backup Degmada Forms
        self.stdout.write('Backing up Degmada Forms...')
        for form in DegmadaForm.objects.all():
            data = {
                'reference': form.reference,
                'date': form.date.isoformat() if form.date else None,
                'company_name': form.company_name,
                'sponsor_name': form.sponsor_name,
                'created_at': form.created_at.isoformat() if form.created_at else None,
            }
            backup_data['degmada_forms'].append(data)
        
        # Backup Kafiilka Forms
        self.stdout.write('Backing up Kafiilka Forms...')
        for form in KafiilkaForm.objects.all():
            data = {
                'reference': form.reference,
                'date': form.date.isoformat() if form.date else None,
                'company_name': form.company_name,
                'sponsor_name': form.sponsor_name,
                'created_at': form.created_at.isoformat() if form.created_at else None,
            }
            backup_data['kafiilka_forms'].append(data)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nBackup completed successfully!\n'
                f'Saved to: {os.path.abspath(output_file)}'
            )
        )

