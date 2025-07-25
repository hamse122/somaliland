# Generated by Django 5.2.4 on 2025-07-20 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DegmadaForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('gobolka', models.CharField(blank=True, max_length=100)),
                ('degmada', models.CharField(blank=True, max_length=100)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('company_license', models.CharField(blank=True, max_length=100)),
                ('establishment_period', models.CharField(blank=True, max_length=100)),
                ('working_employees', models.IntegerField(blank=True, null=True)),
                ('company_region', models.CharField(blank=True, max_length=100)),
                ('company_district', models.CharField(blank=True, max_length=100)),
                ('sponsor_name', models.CharField(blank=True, max_length=200)),
                ('sponsor_id', models.CharField(blank=True, max_length=50)),
                ('sponsor_phone', models.CharField(blank=True, max_length=20)),
                ('sponsor_contact', models.CharField(blank=True, max_length=20)),
                ('sponsor_address', models.TextField(blank=True)),
                ('pledge_name', models.CharField(blank=True, max_length=200)),
                ('pledge_signature', models.CharField(blank=True, max_length=200)),
                ('district_leader_name', models.CharField(blank=True, max_length=200)),
                ('district_leader_signature', models.CharField(blank=True, max_length=200)),
                ('filled_date', models.DateField(blank=True, null=True)),
                ('attachment_types', models.CharField(blank=True, max_length=200)),
                ('special_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='KafiilkaForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('gobolka', models.CharField(blank=True, max_length=100)),
                ('degmada', models.CharField(blank=True, max_length=100)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('company_license', models.CharField(blank=True, max_length=100)),
                ('establishment_period', models.CharField(blank=True, max_length=100)),
                ('working_employees', models.IntegerField(blank=True, null=True)),
                ('company_region', models.CharField(blank=True, max_length=100)),
                ('company_district', models.CharField(blank=True, max_length=100)),
                ('sponsor_type', models.CharField(blank=True, choices=[('SHASI', 'Individual'), ('WADAR', 'Group')], max_length=10)),
                ('sponsor_name', models.CharField(blank=True, max_length=200)),
                ('sponsor_id', models.CharField(blank=True, max_length=50)),
                ('sponsor_phone', models.CharField(blank=True, max_length=20)),
                ('sponsor_contact', models.CharField(blank=True, max_length=20)),
                ('sponsor_address', models.TextField(blank=True)),
                ('pledge_name', models.CharField(blank=True, max_length=200)),
                ('pledge_signature', models.CharField(blank=True, max_length=200)),
                ('district_leader_name', models.CharField(blank=True, max_length=200)),
                ('district_leader_signature', models.CharField(blank=True, max_length=200)),
                ('filled_date', models.DateField(blank=True, null=True)),
                ('attachment_types', models.CharField(blank=True, max_length=200)),
                ('special_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TravelDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_office', models.CharField(blank=True, max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('full_name', models.CharField(blank=True, max_length=200)),
                ('mother_name', models.CharField(blank=True, max_length=200)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('birth_place', models.CharField(blank=True, max_length=100)),
                ('identification_number', models.CharField(blank=True, max_length=50)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('workplace', models.CharField(blank=True, max_length=100)),
                ('sponsor_name', models.CharField(blank=True, max_length=200)),
                ('citizen_card', models.CharField(blank=True, max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('nationality', models.CharField(blank=True, max_length=100)),
                ('district', models.CharField(blank=True, max_length=100)),
                ('job_type', models.CharField(blank=True, max_length=100)),
                ('license_number', models.CharField(blank=True, max_length=50)),
                ('contact_number', models.CharField(blank=True, max_length=20)),
                ('immigration_officer_notes', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('filled', 'Waa la Buxiyay'), ('approved', 'Waa la Ogolaaday'), ('printed', 'Waa la Daabacay')], max_length=10)),
                ('card_number', models.CharField(blank=True, max_length=50)),
                ('officer_signature', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DegmadaFormMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nationality', models.CharField(max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('id_number', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='degmada_photos/')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='immigration.degmadaform')),
            ],
        ),
        migrations.CreateModel(
            name='KafiilkaFormMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nationality', models.CharField(max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(max_length=20)),
                ('id_number', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='kafiilka_photos/')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='immigration.kafiilkaform')),
            ],
        ),
        migrations.CreateModel(
            name='TravelDocumentChild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('birth_place', models.CharField(blank=True, max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='travel_photos/')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='immigration.traveldocument')),
            ],
        ),
    ]
