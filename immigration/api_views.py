"""
API views for the immigration application.
"""
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import TravelDocument, DegmadaForm, KafiilkaForm
from .serializers import (
    TravelDocumentSerializer, TravelDocumentCreateSerializer,
    TravelDocumentUpdateSerializer, DegmadaFormSerializer,
    KafiilkaFormSerializer, StatisticsSerializer,
    DocumentSearchSerializer, ExportRequestSerializer,
    BulkOperationSerializer
)
from .services import (
    TravelDocumentService, FormService, ValidationService,
    ExportService
)
from .utils import ReportGenerator


class TravelDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing travel documents.
    """
    queryset = TravelDocument.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TravelDocumentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TravelDocumentUpdateSerializer
        return TravelDocumentSerializer
    
    def get_queryset(self):
        queryset = TravelDocument.objects.all()
        
        # Filter by query parameters
        query = self.request.query_params.get('query', None)
        region = self.request.query_params.get('region', None)
        status_filter = self.request.query_params.get('status', None)
        
        if query:
            queryset = queryset.filter(
                full_name__icontains=query
            ) | queryset.filter(
                document_number__icontains=query
            )
        
        if region:
            queryset = queryset.filter(region=region)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a travel document."""
        document = self.get_object()
        try:
            updated_document = TravelDocumentService.approve_document(document)
            serializer = self.get_serializer(updated_document)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def print(self, request, pk=None):
        """Mark document as printed."""
        document = self.get_object()
        try:
            updated_document = TravelDocumentService.print_document(document)
            serializer = self.get_serializer(updated_document)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get document statistics."""
        stats = TravelDocumentService.get_document_statistics()
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """Get documents grouped by region."""
        data = ReportGenerator.get_documents_by_region()
        return Response(list(data))
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent documents (last 30 days by default)."""
        days = int(request.query_params.get('days', 30))
        documents = ReportGenerator.get_recent_documents(days)
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Search documents with filters."""
        serializer = DocumentSearchSerializer(data=request.data)
        if serializer.is_valid():
            filters = serializer.validated_data
            documents = TravelDocumentService.search_documents(
                filters.get('query'),
                filters
            )
            page = self.paginate_queryset(documents)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(documents, many=True)
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def export(self, request):
        """Export documents in various formats."""
        serializer = ExportRequestSerializer(data=request.data)
        if serializer.is_valid():
            format_type = serializer.validated_data['format']
            filters = serializer.validated_data.get('filters', {})
            
            documents = TravelDocumentService.search_documents(
                filters.get('query'),
                filters
            )
            
            if format_type == 'excel':
                return ExportService.export_to_excel(documents)
            elif format_type == 'json':
                data = [TravelDocumentSerializer(doc).data for doc in documents]
                from django.http import JsonResponse
                return JsonResponse({'documents': data})
            else:
                return Response(
                    {'error': 'Format not yet implemented'},
                    status=status.HTTP_501_NOT_IMPLEMENTED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['post'])
    def bulk_operation(self, request):
        """Perform bulk operations on documents."""
        serializer = BulkOperationSerializer(data=request.data)
        if serializer.is_valid():
            document_ids = serializer.validated_data['document_ids']
            operation = serializer.validated_data['operation']
            
            documents = TravelDocument.objects.filter(id__in=document_ids)
            results = []
            
            for document in documents:
                try:
                    if operation == 'approve':
                        TravelDocumentService.approve_document(document)
                        results.append({
                            'document_id': document.id,
                            'status': 'success',
                            'message': 'Document approved'
                        })
                    elif operation == 'print':
                        TravelDocumentService.print_document(document)
                        results.append({
                            'document_id': document.id,
                            'status': 'success',
                            'message': 'Document marked as printed'
                        })
                    elif operation == 'delete':
                        document.delete()
                        results.append({
                            'document_id': document.id,
                            'status': 'success',
                            'message': 'Document deleted'
                        })
                except Exception as e:
                    results.append({
                        'document_id': document.id,
                        'status': 'error',
                        'message': str(e)
                    })
            
            return Response({'results': results})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DegmadaFormViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing degmada forms.
    """
    queryset = DegmadaForm.objects.all()
    serializer_class = DegmadaFormSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get degmada form statistics."""
        stats = FormService.get_form_statistics()
        degmada_stats = {
            'total': stats['total_degmada'],
            'recent': stats['recent_degmada']
        }
        return Response(degmada_stats)
    
    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """Validate a degmada form."""
        form = self.get_object()
        errors = FormService.validate_form_completion(form)
        
        if errors:
            return Response(
                {'valid': False, 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'valid': True})


class KafiilkaFormViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing kafiilka forms.
    """
    queryset = KafiilkaForm.objects.all()
    serializer_class = KafiilkaFormSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get kafiilka form statistics."""
        stats = FormService.get_form_statistics()
        kafiilka_stats = {
            'total': stats['total_kafiilka'],
            'recent': stats['recent_kafiilka']
        }
        return Response(kafiilka_stats)
    
    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """Validate a kafiilka form."""
        form = self.get_object()
        errors = FormService.validate_form_completion(form)
        
        if errors:
            return Response(
                {'valid': False, 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'valid': True})


class StatisticsView(generics.RetrieveAPIView):
    """
    View for getting overall statistics.
    """
    serializer_class = StatisticsSerializer
    
    def get(self, request):
        """Get overall statistics."""
        stats = ReportGenerator.get_statistics()
        
        # Combine with service statistics
        travel_stats = TravelDocumentService.get_document_statistics()
        form_stats = FormService.get_form_statistics()
        
        combined_stats = {
            'total_documents': stats['total_travel_documents'],
            'approved_documents': stats['approved_documents'],
            'filled_documents': stats['filled_documents'],
            'printed_documents': stats['printed_documents'],
            'recent_documents': travel_stats['recent_30_days'],
            
            'total_degmada': form_stats['total_degmada'],
            'total_kafiilka': form_stats['total_kafiilka'],
            
            'recent_degmada': form_stats['recent_degmada'],
            'recent_kafiilka': form_stats['recent_kafiilka'],
        }
        
        serializer = StatisticsSerializer(combined_stats)
        return Response(serializer.data)


class DocumentValidationView(generics.CreateAPIView):
    """
    View for validating document data before submission.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """Validate document data."""
        data = request.data
        
        errors = ValidationService.validate_travel_document(data)
        sponsor_errors = ValidationService.validate_sponsor_information(data)
        
        all_errors = errors + sponsor_errors
        
        if all_errors:
            return Response(
                {'valid': False, 'errors': all_errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({'valid': True})

