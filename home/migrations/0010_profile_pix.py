# Generated by Django 4.0.5 on 2022-06-26 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pix',
            field=models.ImageField(default='avatar.png', upload_to='profile'),
        ),
    ]
