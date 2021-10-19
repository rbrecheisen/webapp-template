# Generated by Django 3.2.3 on 2021-10-01 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_taskmodel_error_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilePathModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=2048)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.datasetmodel')),
            ],
        ),
    ]