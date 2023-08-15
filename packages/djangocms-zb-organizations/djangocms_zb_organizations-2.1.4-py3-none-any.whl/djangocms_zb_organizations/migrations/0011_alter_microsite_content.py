# Generated by Django 3.2.11 on 2022-06-02 15:12

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_zb_organizations', '0010_rename_image_catalog_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microsite',
            name='content',
            field=ckeditor.fields.RichTextField(help_text='Content (text) to be displayed on the micro site.', verbose_name='Micro site content'),
        ),
    ]
