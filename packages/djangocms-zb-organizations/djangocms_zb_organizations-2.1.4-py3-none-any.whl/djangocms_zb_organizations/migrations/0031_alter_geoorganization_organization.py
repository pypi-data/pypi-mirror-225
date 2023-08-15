# Generated by Django 3.2.11 on 2022-12-05 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_zb_organizations', '0030_alter_microsite_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoorganization',
            name='organization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='geo_organization', related_query_name='organization', to='djangocms_zb_organizations.organization', verbose_name='Organization'),
        ),
    ]
