from django.urls import path
from . import views

urlpatterns = [
    # Home URL
    path('', views.home, name='home'),
    
    # Degmada Form URLs
    path('degmada/', views.DegmadaFormListView.as_view(), name='degmada_form_list'),
    path('degmada/create/', views.degmada_form_create, name='degmada_form_create'),
    path('degmada/<int:pk>/', views.degmada_form_detail, name='degmada_form_detail'),
    path('degmada/<int:pk>/edit/', views.degmada_form_edit, name='degmada_form_edit'),
    path('degmada/<int:pk>/delete/', views.degmada_form_delete, name='degmada_form_delete'),
    
    # Kafiilka Form URLs
    path('kafiilka/', views.KafiilkaFormListView.as_view(), name='kafiilka_form_list'),
    path('kafiilka/create/', views.kafiilka_form_create, name='kafiilka_form_create'),
    path('kafiilka/<int:pk>/', views.kafiilka_form_detail, name='kafiilka_form_detail'),
    path('kafiilka/<int:pk>/edit/', views.kafiilka_form_edit, name='kafiilka_form_edit'),
    path('kafiilka/<int:pk>/delete/', views.kafiilka_form_delete, name='kafiilka_form_delete'),
    
    # Travel Document URLs
    path('travel/', views.TravelDocumentListView.as_view(), name='travel_document_list'),
    path('travel/create/', views.travel_document_create, name='travel_document_create'),
    path('travel/<int:pk>/', views.travel_document_detail, name='travel_document_detail'),
    path('travel/<int:pk>/edit/', views.travel_document_edit, name='travel_document_edit'),
    path('travel/<int:pk>/delete/', views.travel_document_delete, name='travel_document_delete'),
]