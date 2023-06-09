# Generated by Django 4.2 on 2023-04-28 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Name of the cafe')),
                ('description', models.TextField(verbose_name='Short bio of the cafe')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Menu Item name')),
                ('ingredients', models.CharField(blank=True, max_length=256, null=True, verbose_name='Ingredients used')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Short description of menu item')),
                ('price', models.FloatField(verbose_name='Price')),
                ('active', models.BooleanField(default=True)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.cafe')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('cafe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cafe.cafe')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity of item')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cafe.menuitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.order')),
            ],
        ),
    ]
