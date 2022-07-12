# Generated by Django 4.0.5 on 2022-06-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_contact_message_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('img', models.ImageField(default='prod.jpg', upload_to='product')),
                ('price', models.IntegerField()),
                ('max_quantity', models.IntegerField()),
                ('min_quantity', models.IntegerField()),
                ('display', models.BooleanField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'db_table': 'product',
                'managed': True,
            },
        ),
    ]
