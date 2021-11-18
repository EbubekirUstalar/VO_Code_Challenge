# Generated by Django 3.2.9 on 2021-11-18 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=300)),
                ('required_pcs_fba_send_in_GERMANY', models.IntegerField(default=0)),
                ('required_pcs_fba_send_in_FRANCE', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('Planned', 'Planned'), ('Ordered', 'Ordered'), ('Shipped', 'Shipped'), ('Received', 'Received')], default='Planned', max_length=20)),
                ('warehouse', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_app_1.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='Plain_Carton_Line_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_cartons', models.PositiveIntegerField(default=0)),
                ('cartons_left_cached', models.IntegerField(default=None, null=True)),
                ('pcs_per_carton', models.PositiveIntegerField(default=0)),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app_1.purchase_order')),
                ('sku_obj', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_app_1.sku')),
            ],
        ),
    ]