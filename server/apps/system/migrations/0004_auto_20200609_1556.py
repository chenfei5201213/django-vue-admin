# Generated by Django 3.0.7 on 2020-06-09 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_auto_20200528_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dict',
            old_name='desc',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='dict',
            old_name='pid',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='dicttype',
            old_name='pid',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='historicaldict',
            old_name='desc',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='historicaldict',
            old_name='pid',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='organization',
            old_name='pid',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='permission',
            old_name='pid',
            new_name='parent',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='desc',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='role',
            old_name='desc',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='dict',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='编号'),
        ),
        migrations.AlterField(
            model_name='historicaldict',
            name='code',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='编号'),
        ),
    ]