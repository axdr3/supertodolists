<<<<<<< HEAD
# Generated by Django 3.0.6 on 2020-06-08 13:34
=======
# Generated by Django 3.0.6 on 2020-06-03 21:42
>>>>>>> 2713d1dec2846f734cf206da6bd6aada93331cf2

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0004_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
