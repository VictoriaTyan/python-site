# Generated by Django 3.0 on 2019-12-21 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ourHeadHunter', '0003_response_to_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ourHeadHunter.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ourHeadHunter.Company', verbose_name='Компания'),
        ),
    ]
