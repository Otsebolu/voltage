# Generated by Django 4.0.5 on 2022-06-30 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_shopcart_amount_alter_shopcart_order_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='order_no',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product'),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
