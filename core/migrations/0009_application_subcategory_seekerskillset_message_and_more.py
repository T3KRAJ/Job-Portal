# Generated by Django 4.0.4 on 2022-04-29 13:41
# it was done by tek raj, sai krishna
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_recruiterprofile_job_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('seeker_name', models.CharField(max_length=255)),
                ('cover_letter', models.CharField(max_length=1000)),
                ('cv', models.CharField(max_length=1000)),
                ('matching_score', models.IntegerField()),
                ('status', models.CharField(choices=[('A', 'ACTIVE'), ('S', 'SELECTED'), ('R', 'REJECTED'), {'I', 'Interview'}], default='M', max_length=9)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
                ('seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seekerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(max_length=255)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='SeekerSkillset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_1', models.CharField(max_length=255)),
                ('skill_2', models.CharField(blank=True, max_length=255, null=True)),
                ('skill_3', models.CharField(blank=True, max_length=255, null=True)),
                ('skill_4', models.CharField(blank=True, max_length=255, null=True)),
                ('skill_5', models.CharField(blank=True, max_length=255, null=True)),
                ('seeker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.seekerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.application')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.recruiterprofile')),
                ('seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seekerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview_date', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.application')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subcategory'),
        ),
    ]
