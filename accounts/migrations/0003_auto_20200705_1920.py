# Generated by Django 3.0.7 on 2020-07-05 19:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200705_1823'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='id',
        ),
        migrations.AddField(
            model_name='customuser',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
