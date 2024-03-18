# Generated by Django 4.2.11 on 2024-03-17 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_assistant_user_doctor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='assistant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to='api.assistant'),
        ),
    ]