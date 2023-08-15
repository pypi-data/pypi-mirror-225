from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import huscy.project_consents.models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0003_project_project_manager_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subjects', '0001_squashed_0009_delete_contactold'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectConsent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_fragments', models.JSONField()),
                ('version', models.PositiveIntegerField(default=1)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectConsentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('template_text_fragments', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectConsentToken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('created_by', models.CharField(editable=False, max_length=255, verbose_name='Created by')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.subject')),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectConsentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consent_version', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('filehandle', models.FileField(upload_to=huscy.project_consents.models.get_project_consent_file_upload_path)),
                ('consent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_consents.projectconsent')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.subject')),
            ],
            options={
                'unique_together': {('consent', 'subject', 'consent_version')},
            },
        ),
    ]
