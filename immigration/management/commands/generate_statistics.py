"""
Management command to generate statistics report.
"""
from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from immigration.models import TravelDocument, DegmadaForm, KafiilkaForm


class Command(BaseCommand):
    help = 'Generate and display immigration statistics'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days for recent statistics (default: 30)'
        )

    def handle(self, *args, **options):
        days = options['days']
        
        self.stdout.write(self.style.SUCCESS('\n=== Immigration Statistics ===\n'))
        
        # Travel Documents
        self.stdout.write('Travel Documents:')
        total_docs = TravelDocument.objects.count()
        self.stdout.write(f'  Total: {total_docs}')
        
        status_counts = TravelDocument.objects.values('status').annotate(
            count=Count('id')
        )
        for status in status_counts:
            self.stdout.write(f'  {status["status"]}: {status["count"]}')
        
        cutoff_date = timezone.now() - timedelta(days=days)
        recent_docs = TravelDocument.objects.filter(
            created_at__gte=cutoff_date
        ).count()
        self.stdout.write(f'  Created in last {days} days: {recent_docs}')
        
        # By Region
        region_counts = TravelDocument.objects.values('region').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        if region_counts:
            self.stdout.write(f'\n  Top regions by document count:')
            for region in region_counts:
                if region['region']:
                    self.stdout.write(
                        f'    {region["region"]}: {region["count"]}'
                    )
        
        # Degmada Forms
        self.stdout.write('\nDegmada Forms:')
        total_degmada = DegmadaForm.objects.count()
        self.stdout.write(f'  Total: {total_degmada}')
        
        recent_degmada = DegmadaForm.objects.filter(
            created_at__gte=cutoff_date
        ).count()
        self.stdout.write(f'  Created in last {days} days: {recent_degmada}')
        
        # Kafiilka Forms
        self.stdout.write('\nKafiilka Forms:')
        total_kafiilka = KafiilkaForm.objects.count()
        self.stdout.write(f'  Total: {total_kafiilka}')
        
        recent_kafiilka = KafiilkaForm.objects.filter(
            created_at__gte=cutoff_date
        ).count()
        self.stdout.write(f'  Created in last {days} days: {recent_kafiilka}')
        
        # Summary
        self.stdout.write(f'\n=== Summary ===')
        self.stdout.write(f'Total Records: {total_docs + total_degmada + total_kafiilka}')
        self.stdout.write(
            f'Recent Records ({days} days): {recent_docs + recent_degmada + recent_kafiilka}'
        )
        
        self.stdout.write(self.style.SUCCESS('\nStatistics generated successfully!\n'))

