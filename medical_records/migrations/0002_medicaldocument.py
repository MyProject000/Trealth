# Generated by Django 5.1.7 on 2025-03-20 00:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical_records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalDocument',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='medical_documents/')),
                ('file_name', models.CharField(max_length=255)),
                ('file_type', models.CharField(max_length=100)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('medical_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='medical_records.medicalrecord')),
            ],
        ),
    ]
