# Generated by Django 3.2.5 on 2023-01-05 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_recommender', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='drive_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
