# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-18 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easyrequest_hay_app', '0002_itemrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemrequest',
            name='item_author',
            field=models.CharField(blank=True, help_text='used by Aeon', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_barcode',
            field=models.CharField(blank=True, help_text='used by Millennium', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_bib',
            field=models.CharField(blank=True, help_text='used by Millennium & Aeon', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_callnumber',
            field=models.CharField(blank=True, help_text='used by Millennium & Aeon', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_digital_version_url',
            field=models.CharField(blank=True, help_text='used by Aeon', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_id',
            field=models.CharField(blank=True, help_text='used by Millennium', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_publish_info',
            field=models.CharField(blank=True, help_text='used by Aeon', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='item_title',
            field=models.CharField(blank=True, help_text='used by Millennium & Aeon', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='patron_barcode',
            field=models.CharField(blank=True, help_text='used by Millennium', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='patron_email',
            field=models.CharField(blank=True, help_text='used by Millennium', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='itemrequest',
            name='patron_name',
            field=models.CharField(blank=True, help_text='used by Millennium', max_length=100, null=True),
        ),
    ]