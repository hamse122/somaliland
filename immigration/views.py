from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import (
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember,
    TravelDocument, TravelDocumentChild
)
from .forms import (
    DegmadaFormForm, DegmadaFormMemberFormSet,
    KafiilkaFormForm, KafiilkaFormMemberFormSet,
    TravelDocumentForm, TravelDocumentChildFormSet
)

# Home View
def home(request):
    return render(request, 'base.html')

# Degmada Form Views
class DegmadaFormListView(ListView):
    model = DegmadaForm
    template_name = 'degmada_form/list.html'
    context_object_name = 'forms'

def degmada_form_create(request):
    if request.method == 'POST':
        form = DegmadaFormForm(request.POST, request.FILES)
        formset = DegmadaFormMemberFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            degmada_form = form.save()
            formset.instance = degmada_form
            formset.save()
            return redirect('degmada_form_detail', pk=degmada_form.pk)
    else:
        form = DegmadaFormForm()
        formset = DegmadaFormMemberFormSet()
    
    return render(request, 'degmada_form/create.html', {
        'form': form,
        'formset': formset,
    })

def degmada_form_detail(request, pk):
    form = get_object_or_404(DegmadaForm, pk=pk)
    return render(request, 'degmada_form/detail.html', {'form': form})

def degmada_form_edit(request, pk):
    form_instance = get_object_or_404(DegmadaForm, pk=pk)
    
    if request.method == 'POST':
        form = DegmadaFormForm(request.POST, request.FILES, instance=form_instance)
        formset = DegmadaFormMemberFormSet(request.POST, request.FILES, instance=form_instance)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('degmada_form_detail', pk=pk)
    else:
        form = DegmadaFormForm(instance=form_instance)
        formset = DegmadaFormMemberFormSet(instance=form_instance)
    
    return render(request, 'degmada_form/edit.html', {
        'form': form,
        'formset': formset,
    })

def degmada_form_delete(request, pk):
    form = get_object_or_404(DegmadaForm, pk=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('degmada_form_list')
    return render(request, 'degmada_form/delete.html', {'form': form})

# Kafiilka Form Views
class KafiilkaFormListView(ListView):
    model = KafiilkaForm
    template_name = 'kafiilka_form/list.html'
    context_object_name = 'forms'

def kafiilka_form_create(request):
    if request.method == 'POST':
        form = KafiilkaFormForm(request.POST, request.FILES)
        formset = KafiilkaFormMemberFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            kafiilka_form = form.save()
            formset.instance = kafiilka_form
            formset.save()
            return redirect('kafiilka_form_detail', pk=kafiilka_form.pk)
    else:
        form = KafiilkaFormForm()
        formset = KafiilkaFormMemberFormSet()
    
    return render(request, 'kafiilka_form/create.html', {
        'form': form,
        'formset': formset,
    })

def kafiilka_form_detail(request, pk):
    form = get_object_or_404(KafiilkaForm, pk=pk)
    return render(request, 'kafiilka_form/detail.html', {'form': form})

def kafiilka_form_edit(request, pk):
    form_instance = get_object_or_404(KafiilkaForm, pk=pk)
    
    if request.method == 'POST':
        form = KafiilkaFormForm(request.POST, request.FILES, instance=form_instance)
        formset = KafiilkaFormMemberFormSet(request.POST, request.FILES, instance=form_instance)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('kafiilka_form_detail', pk=pk)
    else:
        form = KafiilkaFormForm(instance=form_instance)
        formset = KafiilkaFormMemberFormSet(instance=form_instance)
    
    return render(request, 'kafiilka_form/edit.html', {
        'form': form,
        'formset': formset,
    })

def kafiilka_form_delete(request, pk):
    form = get_object_or_404(KafiilkaForm, pk=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('kafiilka_form_list')
    return render(request, 'kafiilka_form/delete.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import TravelDocument
from .forms import TravelDocumentForm, TravelDocumentChildFormSet

class TravelDocumentListView(ListView):
    model = TravelDocument
    template_name = 'travel_document/list.html'
    context_object_name = 'documents'

def travel_document_create(request):
    if request.method == 'POST':
        form = TravelDocumentForm(request.POST, request.FILES)
        formset = TravelDocumentChildFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            document = form.save(commit=False)
            # Only set created_by if user is authenticated
            if request.user.is_authenticated:
                document.created_by = request.user
            document.save()
            
            children = formset.save(commit=False)
            for child in children:
                child.document = document
                child.save()
            
            messages.success(request, 'Travel document created successfully!')
            return redirect('travel_document_detail', pk=document.pk)
    else:
        form = TravelDocumentForm()
        formset = TravelDocumentChildFormSet()
    
    return render(request, 'travel_document/form.html', {
        'form': form,
        'formset': formset,
        'title': 'Create Travel Document'
    })

def travel_document_detail(request, pk):
    document = get_object_or_404(TravelDocument, pk=pk)
    return render(request, 'travel_document/detail.html', {'document': document})

def travel_document_edit(request, pk):
    document = get_object_or_404(TravelDocument, pk=pk)
    
    if request.method == 'POST':
        form = TravelDocumentForm(request.POST, request.FILES, instance=document)
        formset = TravelDocumentChildFormSet(request.POST, request.FILES, instance=document)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Travel document updated successfully!')
            return redirect('travel_document_detail', pk=document.pk)
    else:
        form = TravelDocumentForm(instance=document)
        formset = TravelDocumentChildFormSet(instance=document)
    
    return render(request, 'travel_document/form.html', {
        'form': form,
        'formset': formset,
        'title': 'Edit Travel Document'
    })

def travel_document_delete(request, pk):
    document = get_object_or_404(TravelDocument, pk=pk)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Travel document deleted successfully!')
        return redirect('travel_document_list')
    
    return render(request, 'travel_document/delete.html', {'document': document})