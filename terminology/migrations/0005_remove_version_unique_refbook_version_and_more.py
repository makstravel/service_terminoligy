# Generated by Django 5.1.3 on 2025-02-15 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terminology', '0004_alter_element_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='version',
            name='unique_refbook_version',
        ),
        migrations.AlterUniqueTogether(
            name='element',
            unique_together={('version', 'code')},
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together={('refbook', 'version')},
        ),
    ]
