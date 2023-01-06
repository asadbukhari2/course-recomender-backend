# Generated by Django 3.2.5 on 2023-01-06 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('contact_no', models.CharField(max_length=50)),
                ('street_address', models.CharField(blank=True, max_length=100, null=True)),
                ('city_name', models.TextField(max_length=100)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='cars')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudyMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=10, max_digits=19, null=True)),
                ('credit_hours', models.IntegerField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='cars')),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('drive_link', models.URLField(blank=True, max_length=250, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_recommender.category')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_recommender.degree')),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_recommender.difficulty')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_recommender.semester')),
                ('study_mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_recommender.studymode')),
            ],
        ),
    ]
