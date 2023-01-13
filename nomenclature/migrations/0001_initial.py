# Generated by Django 4.1.3 on 2022-12-02 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Approvement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_at', models.DateTimeField(null=True)),
                ('rejected_at', models.DateTimeField(null=True)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Approver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_id', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ens',
            fields=[
                ('number', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('unit', models.CharField(max_length=10)),
                ('okpd', models.CharField(max_length=20)),
                ('okved', models.CharField(max_length=20)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('parent_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='nomenclature.group')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Okpd',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Okved',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('notes', models.TextField(blank=True)),
                ('ens', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nomenclature.ens')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nomenclature.group')),
                ('okpd', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nomenclature.okpd')),
                ('okved', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nomenclature.okved')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('shortname', models.CharField(max_length=10)),
                ('codename', models.CharField(max_length=10)),
                ('shortname_international', models.CharField(max_length=10)),
                ('codename_international', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(null=True)),
                ('views_count', models.IntegerField(default=0)),
                ('person_who_created', models.PositiveBigIntegerField(null=True)),
                ('approvers', models.ManyToManyField(related_name='requests', through='nomenclature.Approvement', to='nomenclature.approver')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='nomenclature.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nomenclature.unit'),
        ),
        migrations.AddField(
            model_name='approvement',
            name='approver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomenclature.approver'),
        ),
        migrations.AddField(
            model_name='approvement',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nomenclature.request'),
        ),
    ]
