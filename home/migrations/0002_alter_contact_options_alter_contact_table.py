# Generated by Django 4.0.5 on 2022-06-07 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'managed': True, 'verbose_name': 'Contact', 'verbose_name_plural': 'Contact'},
        ),
        migrations.AlterModelTable(
            name='contact',
            table='contact',
        ),
    ]
