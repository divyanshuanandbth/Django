# Generated by Django 5.0.6 on 2024-10-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_profile_picture_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='education',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
