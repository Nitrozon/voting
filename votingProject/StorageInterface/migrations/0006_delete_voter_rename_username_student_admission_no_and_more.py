# Generated by Django 5.0.6 on 2024-07-10 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StorageInterface', '0005_voter'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Voter',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='username',
            new_name='admission_no',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='password',
            new_name='name',
        ),
        migrations.AddField(
            model_name='student',
            name='student_class',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
    ]
